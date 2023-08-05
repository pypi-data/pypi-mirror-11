#
# This file is part of ravstack. Ravstack is free software available under
# the terms of the MIT license. See the file "LICENSE" that was provided
# together with this source file for the licensing terms.
#
# Copyright (c) 2015 the ravstack authors. See the file "AUTHORS" for a
# complete list.

"""Ravello Ironic command-line utility.

Usage:
  ravstack [options] config-create
  ravstack [options] proxy-create
  ravstack [options] proxy-run
  ravstack [options] node-create [-c <cpus>] [-m <memory>]
                                [-D <disk>] [-n <count>]
  ravstack [options] node-dump
  ravstack [options] node-list [--all [--cached]]
  ravstack [options] node-start <node>
  ravstack [options] node-stop <node>
  ravstack [options] node-reboot <node>
  ravstack [options] node-get-boot-device <node>
  ravstack [options] node-set-boot-device <node> <bootdev>
  ravstack [options] node-get-macs <node> [--cached]
  ravstack [options] fixup
  ravstack --help

Command help:
  config-create         Create ravstack configuration file.
  proxy-create          Create SSH -> Ravello API proxy.
  proxy-run             Run the API proxy.
  node-create           Create a new node.
  node-dump             Dump node definitions to specified file.
  node-list             List powered on nodes. (--all lists all nodes)
  node-start            Start a node.
  node-stop             Stop a node.
  node-reboot           Reboot a node.
  node-get-boot-device  Return boot device for <node>.
  node-set-boot-device  Set boot device for <node> to <bootdev>.
                        The boot device may be "hd" or "network".
  node-get-macs         Return MAC addresses for <node>.
  fixup                 Fix Ravello and OS config after one or
                        more nodes were deployed.

Options:
  -d, --debug       Enable debugging.
  -v, --verbose     Be verbose (shows logging output on stdout)
  -u <username>, --username=<username>
                    Ravello API username.
  -p <password>, --password=<password>
                    Ravello API password.
  -a <application>, --application=<application>
                    The Ravello application name.
  --all             List all nodes.
  --cached          Allow use of cached information.

Options for `node-create`:
  -c <cpus>, --cpus=<cpus>
                    The number of CPUs. [default: 2]
  -m <memory>, --memory=<memory>
                    The amount of memory in MB. [default: 8192]
  -D <disk>, --disk=<disk>
                    The size of the disk in GB. [default: 60]
  -n <count>, --count=<count>
                    The number of nodes to create. [default: 1]
"""

import sys
import docopt

from . import logging, factory


def _main():
    """Ravstack main entry point."""
    args = docopt.docopt(__doc__)
    env = factory.get_environ(args)

    # On-demand imports for faster startup time.
    # The "proxy-run" command is used a *lot* by Ironic.

    for key, value in args.items():
        if not value:
            continue
        if key.startswith('config-'):
            from . import config
        elif key.startswith('proxy-'):
            from . import proxy
        elif key.startswith('node-'):
            from . import node
        elif key.startswith('fixup'):
            from . import fixup

    if args['config-create']:
        config.do_create(env)
    elif args['proxy-create']:
        proxy.do_create(env)
    elif args['proxy-run']:
        proxy.do_run(env)
    elif args['node-create']:
        node.do_create(env)
    elif args['node-dump']:
        node.do_dump(env)
    elif args['node-list'] and not args.get('--all'):
        node.do_list_running(env, False)
    elif args['node-list']:
        node.do_list_all(env)
    elif args['node-start']:
        node.do_start(env, args['<node>'])
    elif args['node-stop']:
        node.do_stop(env, args['<node>'])
    elif args['node-reboot']:
        node.do_reboot(env, args['<node>'])
    elif args['node-get-boot-device']:
        node.do_get_boot_device(env, args['<node>'])
    elif args['node-set-boot-device']:
        node.do_set_boot_device(env, args['<node>'], args['<bootdev>'])
    elif args['node-get-macs']:
        node.do_get_macs(env, args['<node>'], False)
    elif args['fixup']:
        fixup.do_fixup(env)


def main():
    """Main wrapper function. Calls _main() and handles exceptions."""
    try:
        _main()
    except Exception as e:
        log = logging.get_logger()
        log.error('Uncaught exception:', exc_info=True)
        if logging.get_debug() and not logging.get_verbose():
            raise
        sys.stdout.write('Error: {!s}\n'.format(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
