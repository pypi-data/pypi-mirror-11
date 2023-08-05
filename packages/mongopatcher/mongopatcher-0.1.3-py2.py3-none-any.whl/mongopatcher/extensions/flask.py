#! /usr/bin/env python3

from flask import current_app
from flask.ext.script import Manager, prompt_bool

from mongopatcher import MongoPatcher


def init_patcher(app, db):
    app.config.setdefault('MONGOPATCHER_PATCHES_DIR', 'patches')
    app.config.setdefault('MONGOPATCHER_COLLECTION', 'mongopatcher')
    app.config.setdefault('MONGOPATCHER_APP_VERSION', '0.1.0')
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    if 'mongopatcher' not in app.extensions:
        mp = MongoPatcher(db=db,
                          patches_dir=app.config['MONGOPATCHER_PATCHES_DIR'],
                          collection=app.config['MONGOPATCHER_COLLECTION'])
        app.extensions['mongopatcher'] = mp
    else:
        # Raise an exception if extension already initialized as
        # potentially new configuration would not be loaded.
        raise Exception('Extension already initialized')


patcher_manager = Manager(usage="Perform incremental patch on database")


def _get_mongopatcher():
    extensions = getattr(current_app, 'extensions') or {}
    mongopatcher = extensions.get('mongopatcher')
    if not mongopatcher:
        raise Exception('Extension mongopatcher is not initialized')
    return mongopatcher


@patcher_manager.command
@patcher_manager.option('-y', '--yes', help="Don't ask for confirmation")
@patcher_manager.option('-d', '--dry_run', help="Pretend to do the upgrades")
@patcher_manager.option('-p', '--patches_dir',
                        help="Directory where to find the patches")
def upgrade(yes=False, dry_run=False, patches_dir=None):
    if not patches_dir:
        patches_dir = current_app.config['MONGOPATCHER_PATCHES_DIR']
    patcher = _get_mongopatcher()
    if dry_run:
        patcher.discover_and_apply(patches_dir, dry_run=dry_run)
    else:
        if (yes or prompt_bool("Are you sure you want to alter "
                               " {green}{name}{endc}".format(
                green='\033[92m', name=patcher.db,
                endc='\033[0m'))):
            patcher.discover_and_apply(patches_dir)
        else:
            raise SystemExit('You changed your mind, exiting...')


@patcher_manager.command
@patcher_manager.option('-p', '--patches-dir', dest='patches_dir',
                        help="Directory where to find the patches")
@patcher_manager.option('-v', '--verbose', help="Show patches' descriptions")
@patcher_manager.option('-n', '--name', help="Only look for the given patch")
def discover(patches_dir=None, verbose=False, name=None):
    """List the patches available in the given patches directory"""
    if not patches_dir:
        patches_dir = current_app.config['MONGOPATCHER_PATCHES_DIR']
    patches = _get_mongopatcher().discover(patches_dir)
    if name:
        name = name.split(',')
        patches = [p for p in patches if p.target_version in name]
    if not patches:
        print('No patches found')
    else:
        print('Patches available:')
        for patch in patches:
            if verbose:
                print()
                print(patch.target_version)
                print("~" * len(patch.target_version))
                print('\t' + patch.patchnote.strip().replace('\n', '\n\t'))
            else:
                print(' - %s' % patch.target_version)


@patcher_manager.command
@patcher_manager.option('-f', '--force', help="Overwrite existing manifest")
@patcher_manager.option('-v', '--version', help="Version of the manifest")
def init(version=None, force=False):
    """Initialize mongopatcher manifest on the mongodb database"""
    version = version or current_app.config['MONGOPATCHER_APP_VERSION']
    _get_mongopatcher().manifest.initialize(version, force)
    print('Manifest initialized to version %s' % version)


@patcher_manager.command
@patcher_manager.option('-v', '--verbose', help="Show history")
def info(verbose=False):
    """Show version of the database"""
    if _get_mongopatcher().manifest.is_initialized():
        print('Manifest version: %s' % _get_mongopatcher().manifest.version)
        if verbose:
            print('Update history:')
            for update in reversed(_get_mongopatcher().manifest.history):
                reason = update.get('reason')
                reason = '(%s)' % reason if reason else ''
                print(' - %s: %s %s' % (update['timestamp'], update['version'],
                                        reason))
    else:
        print('No manifest found')


if __name__ == "__main__":
    from flask import Flask
    import pymongo
    app = Flask(__name__)
    db = pymongo.MongoClient('mongodb://localhost:27017/test')
    init_patcher(app, db.get_default_database())
    patcher_manager.app = app
    patcher_manager.run()
