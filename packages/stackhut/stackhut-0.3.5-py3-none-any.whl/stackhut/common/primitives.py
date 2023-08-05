# Copyright 2015 StackHut Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import time
from jinja2 import Environment, FileSystemLoader
from multipledispatch import dispatch
import sh
from distutils.dir_util import copy_tree
import docker as docker_py
from docker.utils import kwargs_from_env
from docker.errors import DockerException
import arrow

from . import utils
from .utils import log
from .barrister import generate_contract

template_env = Environment(loader=FileSystemLoader(utils.get_res_path('templates')))

docker = None

def get_docker(_exit=True):
    try:
        if sys.platform == 'linux':
            docker_client = docker_py.Client(version='auto')
        else:
            docker_client = docker_py.Client(version='auto', **kwargs_from_env(assert_hostname=False))
        return docker_client
    except Exception as e:
        log.error("Could not connect to Docker - try running 'docker info', and if you are on OSX make sure you've run 'boot2docker up' first")
        if _exit:
            sys.exit(1)
        else:
            return None

class DockerBuild:
    def __init__(self, push=False, no_cache=False):
        self.push = push
        self.no_cache = no_cache
        self.docker = get_docker()

    def gen_dockerfile(self, template_name, template_params, dockerfile='Dockerfile'):
        rendered_template = template_env.get_template(template_name).render(template_params)
        with open(dockerfile, 'w') as f:
            f.write(rendered_template)

    def build_dockerfile(self, tag, dockerfile='Dockerfile'):
        log.debug("Running docker build for {}".format(tag))
        cache_flag = '--no-cache=True' if self.no_cache else '--no-cache=False'
        cmds = ['-f', dockerfile, '-t', tag, '--rm', cache_flag, '.']
        log.debug("Calling docker with cmds - {}".format(cmds))
        log.info("Starting build, this may take some time, please wait...")
        sh.docker.build(*cmds)

    def push_image(self, tag):
        if self.push:
            log.info("Uploading image {} - this may take a while...".format(tag))
            self.docker.push(tag)
            # sh.docker('push', tag, _in='Y')

    def stack_build_push(self, template_name, template_params, outdir, image_name):
        """Called by StackHut builders to build BaseOS and Stack images"""
        image_dir = os.path.join(outdir, image_name)
        os.mkdir(image_dir) if not os.path.exists(image_dir) else None

        os.chdir(image_dir)

        self.gen_dockerfile(template_name, template_params)
        # hardcode the service under stackhut name
        tag = "{}/{}:{}".format('stackhut', image_name, 'latest')

        self.build_dockerfile(tag)
        self.push_image(tag)

        os.chdir(utils.ROOT_DIR)


# Base OS's that we support
class BaseOS:
    name = None

    def __init__(self):
        super().__init__()

    @property
    def description(self):
        return "Base OS image using {}".format(self.name.capitalize())

    def build_push(self, outdir, *args):
        log.info("Building image for base {}".format(self.name))
        image_name = self.name
        builder = DockerBuild(*args)
        builder.stack_build_push('Dockerfile-baseos.txt', dict(baseos=self), outdir, image_name)


class Fedora(BaseOS):
    name = 'fedora'

    baseos_pkgs = ['python3', 'python3-pip']

    def os_pkg_cmd(self, pkgs):
        return 'dnf -y install {}'.format(' '.join(pkgs))

    def install_os_pkg(self, pkgs):
        return [
            self.os_pkg_cmd(pkgs),
            'dnf -y autoremove',
            'dnf -y clean all',
            'rm -rf /usr/share/locale/*',
            'rm -rf /usr/share/doc/*',
            'journalctl --vacuum-size=0',
            'rm -rf /var/log/* || true',
            'rm -rf /var/cache/*',
            'rm -rf /tmp/*',
        ]

    def setup_cmds(self):
        return self.install_os_pkg(self.baseos_pkgs)


class Alpine(BaseOS):
    name = 'alpine'

    baseos_pkgs = ['python3', 'ca-certificates']

    def os_pkg_cmd(self, pkgs):
        return 'apk --update add {}'.format(' '.join(pkgs))

    def install_os_pkg(self, pkgs):
        return [
            self.os_pkg_cmd(pkgs),
            'rm -rf /usr/share/locale/*',
            'rm -rf /usr/share/doc/*',
            'rm -rf /var/log/* || true',
            'rm -rf /var/cache/*',
            'rm -rf /tmp/*',
            'mkdir /var/cache/apk',
        ]

    def setup_cmds(self):
        return [
            'echo "@edge http://nl.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories',
            'echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories',
        ] + self.install_os_pkg(self.baseos_pkgs)


# Language stacks that we support
class Stack:
    name = None
    entrypoint = None
    stack_pkgs = None
    package_file = None
    shim_files = None
    shim_cmd = None
    scaffold_name = None

    def __init__(self):
        super().__init__()

    @property
    def description(self):
        return "Support for language stack {}".format(self.name.capitalize())

    def build_push(self, baseos, outdir, *args):
        log.info("Building image for base {} with stack {}".format(baseos.name, self.name))
        image_name = "{}-{}".format(baseos.name, self.name)
        baseos_stack_cmds_pkgs = get_baseos_stack_pkgs(baseos, self)
        if baseos_stack_cmds_pkgs is not None:
            os_cmds, pkgs = baseos_stack_cmds_pkgs
            pkg_cmds = baseos.install_os_pkg(pkgs) if pkgs else []
            stack_cmds = os_cmds + pkg_cmds

            # only render the template if apy supported config
            builder = DockerBuild(*args)
            builder.stack_build_push('Dockerfile-stack.txt',
                                         dict(baseos=baseos, stack=self, stack_cmds=stack_cmds),
                                         outdir, image_name)

    def install_service_pkgs(self):
        """Anything needed to run the service"""
        return ''

    def install_stack_pkgs(self):
        """Anything needed to run the stack"""
        return ''

    @property
    def install_service_file(self):
        return self.package_file if os.path.exists(self.package_file) else ''

    def copy_shim(self):
        shim_dir = os.path.join(utils.get_res_path('shims'), self.name)
        copy_tree(shim_dir, utils.ROOT_DIR)

    def link_shim(self):
        shim_dir = os.path.join(utils.get_res_path('shims'), self.name)
        for f in self.shim_files:
            os.symlink(os.path.join(shim_dir, f), f)

    def del_shim(self):
        for f in self.shim_files:
            os.remove(os.path.join(utils.ROOT_DIR, f))


class Python(Stack):
    name = 'python'
    entrypoint = 'app.py'
    stack_pkgs = ['requests', 'sh']
    package_file = 'requirements.txt'

    shim_files = ['runner.py', 'stackhut.py']
    shim_cmd = ['/usr/bin/env', 'python3', 'runner.py']

    scaffold_name = 'scaffold-python.py'

    def install_stack_pkgs(self):
        return 'pip3 install --no-cache-dir --compile {}'.format(str.join(' ', self.stack_pkgs))

    def install_service_pkgs(self):
        return 'pip3 install --no-cache-dir --compile -r {}'.format(self.package_file)

class Python2(Stack):
    name = 'python2'
    entrypoint = 'app.py'
    stack_pkgs = ['requests', 'sh']
    package_file = 'requirements.txt'

    shim_files = ['runner.py', 'stackhut.py']
    shim_cmd = ['/usr/bin/env', 'python2', 'runner.py']

    scaffold_name = 'scaffold-python2.py'

    def install_stack_pkgs(self):
        return 'pip2 install --no-cache-dir --compile {}'.format(str.join(' ', self.stack_pkgs))

    def install_service_pkgs(self):
        return 'pip2 install --no-cache-dir --compile -r {}'.format(self.package_file)

class NodeJS(Stack):
    name = 'nodejs'
    entrypoint = 'app.js'
    stack_pkgs = ['sync-request']
    package_file = 'package.json'

    shim_files = ['runner.js', 'stackhut.js']
    shim_cmd = ['/usr/bin/env', 'iojs', '--harmony', 'runner.js']

    scaffold_name = 'scaffold-nodejs.js'

    def install_stack_pkgs(self):
        return 'npm install {}'.format(str.join(' ', self.stack_pkgs))

    def install_service_pkgs(self):
        return 'npm install; exit 0'

# Our BaseOS / Stack Dispatchers (e.g. pattern matching)
# we need this as pkds installed per OS are OS dependent
@dispatch(Fedora, Python2)
def get_baseos_stack_pkgs(base_os, stack):
    """return the docker cmds and any os packages needed to be installed"""
    return [], ['python', 'python-pip']

@dispatch(Alpine, Python2)
def get_baseos_stack_pkgs(base_os, stack):
    return [], ['python', 'py-pip']

@dispatch(Fedora, Python)
def get_baseos_stack_pkgs(base_os, stack):
    return [], []  # installed by default

@dispatch(Alpine, Python)
def get_baseos_stack_pkgs(base_os, stack):
    return [], []  # installed by default

@dispatch(Fedora, NodeJS)
def get_baseos_stack_pkgs(base_os, stack):
    cmds = ['dnf -y install dnf-plugins-core',
            'dnf -y copr enable nibbler/iojs',
            ]
    pkgs = ['iojs', 'iojs-npm']
    return cmds, pkgs

@dispatch(Alpine, NodeJS)
def get_baseos_stack_pkgs(base_os, stack):
    return [], ['iojs@testing', 'libstdc++@edge']

@dispatch(object, object)
def get_baseos_stack_pkgs(base_os, stack):
    log.debug("Os / Stack combo for {}/{} not implemented".format(base_os.name, stack.name))
    return None
    # raise NotImplementedError()

bases = dict([(b.name, b) for b in [Alpine(), Fedora()]])
stacks = dict([(s.name, s) for s in [Python(), NodeJS(), Python2()]])

def is_stack_supported(base, stack):
    """Return true if the baseos & stack combination is supported"""
    if get_baseos_stack_pkgs(base, stack) is not None:
        return True
    else:
        return False

class Service:
    """Main primitive representing a StackHut service"""
    def __init__(self, hutcfg, usercfg):
        super().__init__()

        self.hutcfg = hutcfg
        self.usercfg = usercfg
        self.baseos = bases[hutcfg.baseos]
        self.stack = stacks[hutcfg.stack]
        self.from_image = "{}-{}".format(self.baseos.name, self.stack.name)

    @property
    def build_date(self):
        return int(time.time())

    @property
    def image_exists(self):
        return (True if len(get_docker().images(self.hutcfg.repo)) > 0 else False)

    def _files_mtime(self):
        """Recurse over all files referenced by project and find max mtime"""
        def max_mtime(dirpath, fnames):
            """return max mtime from list of files in a dir"""
            mtimes = (os.path.getmtime(os.path.join(dirpath, fname)) for fname in fnames)
            return max(mtimes)

        def max_mtime_dir(dirname):
            """find max mtime of a single file in dir recurseively"""
            for (dirpath, dirnames, fnames) in os.walk(dirname):
                log.debug("Walking dir {}".format(dirname))
                yield max_mtime(dirpath, fnames)

        stack = stacks[self.hutcfg.stack]
        default_files = [stack.entrypoint, stack.package_file, 'api.idl', 'Hutfile']

        # find the max - from default files, hut file and hut dirs
        max_mtime_default_files = max_mtime(os.getcwd(), default_files)
        max_mtime_hutfiles = max_mtime(os.getcwd(), self.hutcfg.files) if self.hutcfg.files else 0
        max_mtime_hutdirs = max((max_mtime_dir(dirname) for dirname in self.hutcfg.dirs)) if self.hutcfg.dirs else 0

        return max([max_mtime_default_files, max_mtime_hutfiles, max_mtime_hutdirs])

    def image_stale(self):
        """Runs the build only if a file has changed"""
        max_mtime = self._files_mtime()

        repo = self.hutcfg.repo

        image_info = get_docker().inspect_image(repo)
        image_build_string = image_info['Created']

        log.debug("Image {} last built at {}".format(repo, image_build_string))
        build_date = arrow.get(image_build_string).datetime.timestamp()
        log.debug("Files max mtime is {}, image build date is {}".format(max_mtime, build_date))

        return max_mtime >= build_date

    def build_push(self, force, *args):
        """Builds a user service, if changed, and pushes  to repo if requested"""
        builder = DockerBuild(*args)
        service_name = self.hutcfg.service

        if force or not self.image_exists or self.image_stale():
            log.debug("Image not found or stale - building...")
            # setup
            gen_barrister_contract()
            dockerfile = os.path.join(utils.STACKHUT_DIR, 'Dockerfile')
            builder.gen_dockerfile('Dockerfile-service.txt', dict(service=self), dockerfile)
            builder.build_dockerfile(service_name, dockerfile)

            log.info("{} build complete".format(self.hutcfg.name))
        else:
            log.info("Build not necessary, run with '--force' to override")

        builder.push_image(service_name)


# Helper functions
# TODO - we should move these into a dep-style system - maybe use Makefile in interrim
def gen_barrister_contract():
    generate_contract('api.idl', utils.CONTRACTFILE)
