#!/usr/bin/env python
import os, pty, shlex, uuid, fcntl, termios, sys
from walt.common.io import SmartBufferingFileReader, \
                            unbuffered, read_and_copy
from walt.common.tcp import REQ_SQL_PROMPT, REQ_DOCKER_PROMPT, \
                            REQ_NODE_SHELL, REQ_DEVICE_PING, \
                            read_pickle

class PromptProcessListener(object):
    def __init__(self, slave_r, slave_w, sock_file_r, sock_file_w):
        self.slave_r = slave_r
        self.slave_w = slave_w
        self.sock_file_r = sock_file_r
        self.sock_file_w = sock_file_w
        self.slave_reader = SmartBufferingFileReader(slave_r)
    # let the event loop know what we are reading on
    def fileno(self):
        return self.slave_r.fileno()
    # when the event loop detects an event for us, this means
    # the slave proces wrote something on its output
    # we just have to copy this to the user socket
    def handle_event(self, ts):
        return read_and_copy(
                self.slave_reader, self.sock_file_w)
    def close(self):
        # note: if we close, we want the other listener
        # (PromptSocketListener) to close too.
        # that's why we kept a reference to sock_file_r
        # and slave_w, closing them should achieve what
        # we want.
        self.sock_file_r.close()
        self.sock_file_w.close()
        self.slave_r.close()
        self.slave_w.close()

class PromptSocketListener(object):
    def __init__(self, ev_loop, sock_file, **kwargs):
        self.ev_loop = ev_loop
        self.win_size = None
        self.cmd = None
        # use unbuffered reading & writing on the socket
        self.sock_file_r = unbuffered(sock_file, 'r')
        self.sock_file_w = unbuffered(sock_file, 'w')
        self.slave_r = None
        self.slave_w = None
    def get_command(self):
        '''this should be defined in subclasses'''
        raise NotImplementedError
    def start(self):
        self.slave_pid, fd_slave = pty.fork()
        # the child (slave process) should execute the command
        if self.slave_pid == 0:
            # set the window size appropriate for the remote client
            fcntl.ioctl(sys.stdout.fileno(), termios.TIOCSWINSZ, self.win_size)
            env = os.environ.copy()
            env.update({'TERM':'xterm'})
            cmd_args = shlex.split(self.cmd)
            os.execvpe(cmd_args[0], cmd_args, env)
        # the parent should communicate.
        # use unbuffered communication with the slave process
        self.slave_r = os.fdopen(os.dup(fd_slave), 'r', 0)
        self.slave_w = os.fdopen(os.dup(fd_slave), 'w', 0)
        # provide read_available() method on the socket
        self.sock_reader = SmartBufferingFileReader(self.sock_file_r)
        # create a new listener on the event loop for reading
        # what the slave process outputs
        process_listener = PromptProcessListener(
                    self.slave_r, self.slave_w,
                    self.sock_file_r, self.sock_file_w)
        self.ev_loop.register_listener(process_listener)
    # let the event loop know what we are reading on
    def fileno(self):
        if self.sock_file_r.closed:
            return None
        return self.sock_file_r.fileno()
    # handle_event() will be called when the event loop detects
    # new input data for us.
    def handle_event(self, ts):
        if self.win_size == None:
            # we did not read the window size yet, let's do it
            self.win_size = read_pickle(self.sock_file_r)
            if self.win_size == None:
                self.close()    # issue
        elif self.cmd == None:
            # we did not compute the command to be run yet, let's do it
            self.cmd = self.get_command()
            if self.cmd == None:
                self.close()    # issue
                return
            # we now have all info to start the child process
            self.start()
        else:
            # otherwise we are all set. Thus, getting input data means
            # the user wrote something on the prompt (i.e. the socket)
            # we just have to copy this to the slave process input
            return read_and_copy(
                self.sock_reader, self.slave_w)
    def close(self):
        self.sock_file_r.close()
        self.sock_file_w.close()
        if self.slave_r:
            self.slave_r.close()
        if self.slave_w:
            self.slave_w.close()

class SQLPromptSocketListener(PromptSocketListener):
    REQ_ID = REQ_SQL_PROMPT
    def get_command(self):
        return 'psql walt'

class DockerPromptSocketListener(PromptSocketListener):
    REQ_ID = REQ_DOCKER_PROMPT
    def get_command(self):
        image, container = read_pickle(self.sock_file_r)
        return 'docker run -it --entrypoint %s -h %s --name %s %s' % \
                       ('/bin/bash', 'image-shell',
                        container, image)

class NodeShellSocketListener(PromptSocketListener):
    REQ_ID = REQ_NODE_SHELL
    def get_command(self):
        node_ip = read_pickle(self.sock_file_r)
        return 'ssh -o StrictHostKeyChecking=no root@%s' % node_ip

class DevicePingSocketListener(PromptSocketListener):
    REQ_ID = REQ_DEVICE_PING
    def get_command(self):
        device_ip = read_pickle(self.sock_file_r)
        return 'ping %s' % device_ip

class InteractionManager(object):
    def __init__(self, tcp_server, ev_loop):
        for cls in [    SQLPromptSocketListener,
                        DockerPromptSocketListener,
                        NodeShellSocketListener,
                        DevicePingSocketListener ]:
            tcp_server.register_listener_class(
                    req_id = cls.REQ_ID,
                    cls = cls,
                    ev_loop = ev_loop)

