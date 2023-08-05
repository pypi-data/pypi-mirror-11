#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import argparse
import sys
from stackhut import __version__
from stackhut.common import utils
from stackhut.common.utils import log
import stackhut.toolkit
import stackhut.runner

COMMANDS = stackhut.toolkit.COMMANDS + stackhut.runner.COMMANDS

def main():
    # Parse the cmd args
    parser = argparse.ArgumentParser(description="StackHut Toolkit",
                                     epilog="Have fun :)")
    parser.add_argument('-V', help='StackHut Toolkit Version',
                        action="version", version="%(prog)s {}".format(__version__))
    #    parser.add_argument("--hutfile", help="Path to user-defined hutfile (default: %(default)s)",
    #                        default=utils.HUTFILE, type=argparse.FileType('r', encoding='utf-8'))
    parser.add_argument('-v', dest='verbose', help="Verbosity level, add multiple times to increase",
                        action='count', default=0)
    parser.add_argument('-d', dest='debug', help=argparse.SUPPRESS)

    # build the subparsers
    metavar = '{{{}}}'.format(str.join(',', [cmd.name for cmd in COMMANDS if cmd.visible]))
    subparsers = parser.add_subparsers(title="StackHut Commands", dest='command', metavar=metavar)
    [cmd.parse_cmds(subparsers) for cmd in COMMANDS]

    # parse the args
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        parser.exit(0, "No command given\n")

    # General App Setup
    utils.DEBUG = args.debug
    utils.set_log_level(args.verbose)
    log.info("Starting up StackHut")
    log.debug(args)

    # dispatch to correct subfunction - i.e. build, compile, run, etc.
    subfunc = args.func(args)
    retval = subfunc.run()

    # all done
    return retval


if __name__ == '__main__':
    retval = main()
    sys.exit(retval)
