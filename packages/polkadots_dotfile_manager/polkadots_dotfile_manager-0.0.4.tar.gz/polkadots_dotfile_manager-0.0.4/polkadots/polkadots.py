import json
import sys
import os
import os.path
import abc
import argparse
import logging
from . import version


CONFIG_LOCATION = os.path.expanduser('~/.config/polkadots/config.json')


class MissingActionError(Exception):
    pass


class NotALinkError(Exception):
    pass


class Action(metaclass=abc.ABCMeta):

    def __init__(self, dotfile_repo, **args):
        """
        Instantiate an Action.

        Positional arguments:
        The dotfile repository

        Keyword arguments:
        Whatever's in the config file for this Action
        """
        pass

    def execute(self):
        """
        Execute an action and throw an exception if it fails
        """
        pass


class SymlinkAction(Action):

    def __init__(self, dotfile_repo, **args):
        """
        Instantiate a SymlinkAction

        Positional arguments:
        dotfile_repo -- the dotfile repository. Make everything relative to
                        this.

        Keyword Arguments:
        dir_mode -- symlink everything in the source directory to the same
                    names in the destination directory?
        source -- source file/directory
        destination -- destination file/directory
        """
        self.dir_mode = args.get('dir_mode', False)
        self.source = get_intuitive_path(args['source'], base=dotfile_repo)
        self.destination = get_intuitive_path(args['destination'],
                                              base=dotfile_repo)

    def execute(self):
        if self.dir_mode:
            for f in os.listdir(self.source):
                fdest = os.path.join(self.destination, f)
                fsource = os.path.join(self.source, f)
                rmlink(fdest, ignore_absent=True)
                os.symlink(fsource, fdest)
        else:
            rmlink(self.destination, ignore_absent=True)
            os.symlink(self.source, self.destination)


def rmlink(link, ignore_absent=False):
    if os.path.islink(link):
        logging.info('Deleting {}'.format(link))
        os.remove(link)
    elif not os.path.exists(link):
        logging.debug('File missing when trying to delete {}'.format(link))
        if not ignore_absent:
            raise FileNotFoundError('{} when attempting to delete it as '
                                    'a link'.format(link))
    else:
        raise NotALinkError('Found that {} is not a link when attempting '
                            'overwrite. Please fix your config or '
                            'move this file'.format(link))


def get_intuitive_path(path, base='.'):
    """
    Take a path and get the absolute, user expanded, variable expanded version
    """
    os.chdir(os.path.abspath(os.path.expanduser(os.path.expandvars(base))))
    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


def load_conf(f):
    """
    Load a JSON based config file/directory

    Returns: a dictionary with the unserialized config
    """
    conf = {}
    if os.path.isdir(f):
        for name in os.listdir(f):
            with open(name) as h:
                conf.update(json.loads(h.read()))
    else:
        with open(f) as h:
            conf.update(json.loads(h.read()))
    return conf


def get_actions(action_list, dotfile_repo):
    actions = []
    for action in action_list:
        try:
            logging.info('Processing {}'.format(action['type']))
            klass = getattr(sys.modules[__name__], action['type'])
            actions.append(klass(dotfile_repo=dotfile_repo, **action))
        except:
            logging.error('Error creating Action {}. It might not be '
                          'implemented'.format(action['type']))
            raise
    return actions


def get_config(config=CONFIG_LOCATION):
    if not config:
        config = CONFIG_LOCATION
    if os.path.exists(config) and os.path.isfile(config):
        logging.info('Loading config from {}'.format(config))
        return load_conf(config)
    else:
        logging.error('No config found in {}'.format(config))
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description='Yet another dotfile manager')
    ap.add_argument('--verbose', '-v', action='count', default=0)
    ap.add_argument('--config', '-c', help='Config to use rather than the '
                    'default. Can be a directory')
    ap.add_argument('--version', action='store_true')
    args = ap.parse_args()

    if args.version:
        print(version.version)
        sys.exit(0)

    log_level = logging.WARNING

    if args.verbose == 1:
        log_level = logging.INFO
    elif args.verbose >= 2:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)

    conf = get_config(args.config)
    actions = get_actions(conf['actions'], conf['dotfile_repo'])
    for action in actions:
        action.execute()


if __name__ == '__main__':
    main()
