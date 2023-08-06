from docker import Client
from plumbum.cmd import mount, umount, findmnt
from network import nfs
from network.tools import get_server_ip
from walt.server.tools import columnate
from walt.common.tools import \
        failsafe_makedirs, failsafe_symlink, succeeds
from walt.server import const
import os, re, sys, requests, uuid, shlex, time
from datetime import datetime

IMAGE_IS_USED_BUT_NOT_FOUND=\
    "WARNING: image %s is not found. Cannot attach it to related nodes.\n"
IMAGE_MOUNT_PATH='/var/lib/walt/images/%s/fs'
CONFIG_ITEM_DEFAULT_IMAGE='default_image'
SERVER_PUBKEY_PATH = '/root/.ssh/id_dsa.pub'
HOSTS_FILE_CONTENT="""\
127.0.0.1   localhost
::1     localhost ip6-localhost ip6-loopback
ff02::1     ip6-allnodes
ff02::2     ip6-allrouters
"""

def get_mount_path(image_name):
    return IMAGE_MOUNT_PATH % \
            re.sub('[^a-zA-Z0-9/-]+', '_', re.sub(':', '/', image_name))

def get_server_pubkey():
    with open(SERVER_PUBKEY_PATH, 'r') as f:
        return f.read()

class ModifySession(object):
    def __init__(self, requester, docker_image_name, image_name, repo):
        self.requester = requester
        self.docker_image_name = docker_image_name
        self.image_name = image_name
        self.new_image_name = None
        self.repo = repo
        self.container_name = str(uuid.uuid4())
        self.repo.register_modify_session(self)
        # expose methods to the RPyC client
        self.exposed___enter__ = self.__enter__
        self.exposed___exit__ = self.__exit__
        self.exposed_get_parameters = self.get_parameters
        self.exposed_get_default_new_name = self.get_default_new_name
        self.exposed_validate_new_name = self.validate_new_name
        self.exposed_select_new_name = self.select_new_name
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.repo.finalize_modify(self)
    def get_parameters(self):
        # return an immutable object (a tuple, not a dict)
        # otherwise we will cause other RPyC calls
        return self.docker_image_name, self.container_name
    def get_default_new_name(self):
        return self.repo.get_default_new_image_name(
            self.image_name
        )
    def validate_new_name(self, new_image_name):
        return self.repo.validate_new_image_name(
            self.requester,
            new_image_name
        )
    def select_new_name(self, new_image_name):
        self.new_image_name = new_image_name

class NodeImage(object):
    server_pubkey = get_server_pubkey()
    REMOTE = 0
    LOCAL = 1
    def __init__(self, c, name, state):
        self.c = c
        self.rename(name)
        self.set_created_at()
        self.state = state
        self.cid = None
        self.mount_path = None
        self.mounted = False
        self.server_ip = get_server_ip()
    def rename(self, name):
        parts = name.split(':')
        if len(parts) == 1:
            self.name, self.tag = name, 'latest'
        else:
            self.name, self.tag = parts
        self.docker_user = name.split('/')[0]
        self.tagged_name = name
    def set_created_at(self):
        # created_at is only available on local images
        # (downloaded or created locally)
        self.created_at = None
        for i in self.c.images():
            if self.tagged_name in i['RepoTags']:
                self.created_at = datetime.fromtimestamp(i['Created'])
    def __del__(self):
        if self.mounted:
            self.unmount()
    def download(self):
        for idx, line in enumerate(
                    self.c.pull(
                        self.name,
                        tag=requests.utils.quote(self.tag),
                        stream=True)):
            progress = "-/|\\"[idx % 4]
            sys.stdout.write('Downloading image %s... %s\r' % \
                                (self.tagged_name, progress))
            sys.stdout.flush()
        sys.stdout.write('\n')
        self.state = NodeImage.LOCAL
    def get_mount_path(self):
        return get_mount_path(self.tagged_name)
    def docker_command_split(self, cmd):
        args = shlex.split(cmd)
        return dict(
            entrypoint=args[0],
            command=args[1:]
        )
    def mount(self):
        print 'Mounting %s...' % self.tagged_name,
        self.mount_path = self.get_mount_path()
        failsafe_makedirs(self.mount_path)
        if self.state == NodeImage.REMOTE:
            self.download()
        params = dict(image=self.tagged_name)
        params.update(self.docker_command_split(
            'walt-node-install %s "%s"' % \
                    (self.server_ip, NodeImage.server_pubkey)))
        self.cid = self.c.create_container(**params).get('Id')
        self.c.start(container=self.cid)
        self.bind_mount()
        self.create_hosts_file()
        self.mounted = True
        print 'done'
    def unmount(self):
        print 'Un-mounting %s...' % self.tagged_name,
        while not succeeds('umount %s 2>/dev/null' % self.mount_path):
            time.sleep(0.1)
        self.c.kill(container=self.cid)
        self.c.wait(container=self.cid)
        self.c.remove_container(container=self.cid)
        os.rmdir(self.mount_path)
        self.mounted = False
        print 'done'
    def create_hosts_file(self):
        # since file /etc/hosts is managed by docker,
        # it appears empty on the bind mount.
        # let's create it appropriately.
        with open(self.mount_path + '/etc/hosts', 'w') as f:
            f.write(HOSTS_FILE_CONTENT)
    def list_mountpoints(self):
        return findmnt('-nlo', 'TARGET').splitlines()
    def get_mount_point(self):
        return [ line for line in self.list_mountpoints() \
                        if line.find(self.cid) != -1 ][0]
    def bind_mount(self):
        mount('-o', 'bind', self.get_mount_point(), self.mount_path)

class NodeImageRepository(object):
    def __init__(self, db):
        self.db = db
        self.c = Client(base_url='unix://var/run/docker.sock', version='auto')
        self.images = {}
        self.modify_sessions = set()
        self.add_local_images()
        self.add_remote_images()
    def add_local_images(self):
        local_images = sum([ i['RepoTags'] for i in self.c.images() ], [])
        for name in local_images:
            if '/walt-node' in name:
                self.images[name] = NodeImage(self.c, name, NodeImage.LOCAL)
    def lookup_remote_tags(self, image_name):
        url = const.DOCKER_HUB_GET_TAGS_URL % dict(image_name = image_name)
        r = requests.get(url)
        for elem in requests.get(url).json():
            tag = requests.utils.unquote(elem['name'])
            yield "%s:%s" % (image_name, tag)
    def add_remote_images(self):
        current_names = set(self.images.keys())
        remote_names = set([])
        for result in self.c.search(term='walt-node'):
            if '/walt-node' in result['name']:
                for tagged_image in self.lookup_remote_tags(result['name']):
                    remote_names.add(tagged_image)
        for name in (remote_names - current_names):
            self.images[name] = NodeImage(self.c, name, NodeImage.REMOTE)
    def __getitem__(self, key):
        return self.images[key]
    def __iter__(self):
        return self.images.iterkeys()
    def update_image_mounts(self):
        images_in_use = self.get_images_in_use()
        images_found = []
        # ensure all needed images are mounted
        for name in images_in_use:
            if name in self.images:
                img = self.images[name]
                if not img.mounted:
                    img.mount()
                images_found.append(img)
            else:
                sys.stderr.write(IMAGE_IS_USED_BUT_NOT_FOUND % name)
        # update default image link
        self.update_default_link()
        # update nfs configuration
        nfs.update_exported_filesystems(images_found)
        # unmount images that are not needed anymore
        for name in self.images:
            if name not in images_in_use:
                img = self.images[name]
                if img.mounted:
                    img.unmount()
    def cleanup(self):
        # give up modify sessions
        for session in self.modify_sessions.copy():
            self.cleanup_modify_session(session)
        # release nfs mounts
        nfs.update_exported_filesystems([])
        # unmount images
        for name in self.images:
            img = self.images[name]
            if img.mounted:
                img.unmount()
    def get_images_in_use(self):
        res = set([ item.image for item in \
            self.db.execute("""
                SELECT DISTINCT image FROM nodes""").fetchall()])
        res.add(self.get_default_image())
        return res
    def get_default_image(self):
        if len(self.images) > 0:
            default_if_not_specified = self.images.keys()[0]
        else:
            default_if_not_specified = None
        return self.db.get_config(
                    CONFIG_ITEM_DEFAULT_IMAGE,
                    default_if_not_specified)
    def update_default_link(self):
        default_image = self.get_default_image()
        default_mount_path = get_mount_path(default_image)
        default_simlink = get_mount_path('default')
        failsafe_makedirs(default_mount_path)
        failsafe_symlink(default_mount_path, default_simlink)
    def get_image_from_tag(self, image_tag, requester = None):
        for image in self.images.values():
            if image.tag == image_tag:
                return image
        if requester:
            requester.stderr.write(
                "No such image '%s'. (tip: walt image show)\n" % image_tag)
        return None
    def has_image(self, requester, image_tag):
        return self.get_image_from_tag(image_tag, requester) != None
    def set_image(self, requester, node_mac, image_tag):
        image = self.get_image_from_tag(image_tag, requester)
        if image:
            self.db.update('nodes', 'mac',
                    mac=node_mac,
                    image=image.tagged_name)
            self.update_image_mounts()
            self.db.commit()
    def describe(self):
        tabular_data = []
        header = [ 'Name', 'Origin', 'Mounted', 'Default', 'Created' ]
        default = self.get_default_image()
        missing_created_at = False
        for name, image in self.images.iteritems():
            created_at = image.created_at
            if not created_at:
                created_at = 'N/A (1)'
                missing_created_at = True
            tabular_data.append([
                        image.tag,
                        image.docker_user,
                        str(image.mounted),
                        '*' if name == default else '',
                        created_at])
        res = columnate(tabular_data, header)
        if missing_created_at:
            res += '\n\n(1): no info about creation date for remote images.'
        return res
    def set_default(self, requester, image_tag):
        image = self.get_image_from_tag(image_tag, requester)
        if image:
            self.db.set_config(
                    CONFIG_ITEM_DEFAULT_IMAGE,
                    image.tagged_name)
            self.update_image_mounts()
            self.db.commit()
    def create_modify_session(self, requester, image_tag):
        image = self.get_image_from_tag(image_tag, requester)
        if not image:
            requester.stderr.write('No such image.\n')
            return None
        else:
            return ModifySession(requester, image.tagged_name, image_tag, self)
    def get_default_new_image_name(self, old_image_tag):
        new_tag = old_image_tag
        while self.get_image_from_tag(new_tag):
            new_tag += '_new'
        return new_tag
    def validate_new_image_name(self, requester, new_image_tag):
        if self.get_image_from_tag(new_image_tag):
            requester.stderr.write('Bad name: Image already exists.\n')
            return False
        if not re.match('^[a-zA-Z0-9\-_]+$', new_image_tag):
            requester.stderr.write(\
                'Bad name: Only alnum, dash(-) and underscore(_) characters are allowed.\n')
            return False
        return True
    def register_modify_session(self, session):
        self.modify_sessions.add(session)
    def cleanup_modify_session(self, session):
        cname = session.container_name
        # kill/remove the container if it ever existed
        try:
            self.c.kill(container=cname)
        except:
            pass
        try:
            self.c.wait(container=cname)
        except:
            pass
        try:
            self.c.remove_container(container=cname)
        except:
            pass
        self.modify_sessions.remove(session)
    def finalize_modify(self, session):
        requester = session.requester
        new_image_tag = session.new_image_name
        container_name = session.container_name
        if new_image_tag:
            self.c.commit(
                    container=container_name,
                    repository='local/walt-node',
                    tag=new_image_tag,
                    message='Image modified using walt image modify')
            full_name = 'local/walt-node:%s' % new_image_tag
            self.images[full_name] = NodeImage(self.c, full_name, NodeImage.LOCAL)
            requester.stdout.write('New image %s saved.\n' % new_image_tag)
        self.cleanup_modify_session(session)
    def get_local_unmounted_image_from_tag(self, image_tag, requester):
        image = self.get_image_from_tag(image_tag, requester)
        if image:   # otherwise issue is already reported
            if image.docker_user != 'local':
                requester.stderr.write('Sorry, this operation is allowed on local images only.\n')
                return None
            if image.mounted:
                requester.stderr.write('Sorry, cannot proceed because the image is mounted.\n')
                return None
        return image

    def remove(self, requester, image_tag):
        image = self.get_local_unmounted_image_from_tag(image_tag, requester)
        if image:   # otherwise issue is already reported
            name = image.tagged_name
            del self.images[name]
            self.c.remove_image(
                    image=name, force=True)

    def rename(self, requester, image_tag, new_tag):
        image = self.get_local_unmounted_image_from_tag(image_tag, requester)
        if image:   # otherwise issue is already reported
            if self.get_image_from_tag(new_tag):
                requester.stderr.write('Bad name: Image already exists.\n')
                return
            name = image.tagged_name
            new_name = 'local/walt-node:' + new_tag
            # update image internal attributes
            image.rename(new_name)
            # rename in this repo
            self.images[new_name] = image
            del self.images[name]
            # rename the docker image
            self.c.tag(image=name, repository='local/walt-node', tag=new_tag)
            self.c.remove_image(image=name, force=True)
