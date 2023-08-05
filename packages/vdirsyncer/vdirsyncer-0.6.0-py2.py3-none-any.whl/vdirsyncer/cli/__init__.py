# -*- coding: utf-8 -*-

import functools
import sys

from .. import __version__, log
from ..doubleclick import click, ctx


cli_logger = log.get(__name__)


class CliError(RuntimeError):
    def __init__(self, msg, problems=None):
        self.msg = msg
        self.problems = problems
        RuntimeError.__init__(self, msg)

    def format_cli(self):
        msg = self.msg.rstrip(u'.:')
        if self.problems:
            msg += u':'
            if len(self.problems) == 1:
                msg += u' {}'.format(self.problems[0])
            else:
                msg += u'\n' + u'\n  - '.join(self.problems) + u'\n\n'

        return msg


def catch_errors(f):
    @functools.wraps(f)
    def inner(*a, **kw):
        try:
            f(*a, **kw)
        except:
            from .utils import handle_cli_error
            handle_cli_error()
            sys.exit(1)

    return inner


def validate_verbosity(ctx, param, value):
    x = getattr(log.logging, value.upper(), None)
    if x is None:
        raise click.BadParameter(
            'Must be CRITICAL, ERROR, WARNING, INFO or DEBUG, not {}'
            .format(value)
        )
    return x


@click.group()
@click.option('--verbosity', '-v', default='INFO',
              callback=validate_verbosity,
              help='Either CRITICAL, ERROR, WARNING, INFO or DEBUG')
@click.version_option(version=__version__)
@catch_errors
def app(verbosity):
    '''
    vdirsyncer -- synchronize calendars and contacts
    '''
    from .utils import load_config
    log.add_handler(log.stdout_handler)
    log.set_level(verbosity)

    if ctx.obj is None:
        ctx.obj = {}

    ctx.obj['verbosity'] = verbosity

    if 'config' not in ctx.obj:
        ctx.obj['config'] = load_config()

main = app


def max_workers_callback(ctx, param, value):
    if value == 0 and ctx.obj['verbosity'] == log.logging.DEBUG:
        value = 1

    cli_logger.debug('Using {} maximal workers.'.format(value))
    return value


max_workers_option = click.option(
    '--max-workers', default=0, type=click.IntRange(min=0, max=None),
    callback=max_workers_callback,
    help=('Use at most this many connections. With debug messages enabled, '
          'the default is 1, otherwise one connection per collection is '
          'opened.')
)


@app.command()
@click.argument('pairs', nargs=-1)
@click.option('--force-delete/--no-force-delete',
              help=('Do/Don\'t abort synchronization when all items are about '
                    'to be deleted from both sides.'))
@max_workers_option
@catch_errors
def sync(pairs, force_delete, max_workers):
    '''
    Synchronize the given pairs. If no arguments are given, all will be
    synchronized.

    This command will not synchronize metadata, use `vdirsyncer metasync` for
    that.

    Examples:

        `vdirsyncer sync` will sync everything configured.

        `vdirsyncer sync bob frank` will sync the pairs "bob" and "frank".

        `vdirsyncer sync bob/first_collection` will sync "first_collection"
        from the pair "bob".
    '''
    from .tasks import prepare_pair, sync_collection
    from .utils import parse_pairs_args, WorkerQueue
    general, all_pairs, all_storages = ctx.obj['config']

    wq = WorkerQueue(max_workers)

    for pair_name, collections in parse_pairs_args(pairs, all_pairs):
        wq.put(functools.partial(prepare_pair, pair_name=pair_name,
                                 collections=collections,
                                 general=general, all_pairs=all_pairs,
                                 all_storages=all_storages,
                                 force_delete=force_delete,
                                 callback=sync_collection))
        wq.spawn_worker()

    wq.join()


@app.command()
@click.argument('pairs', nargs=-1)
@max_workers_option
@catch_errors
def metasync(pairs, max_workers):
    '''
    Synchronize metadata of the given pairs.

    See the `sync` command regarding the PAIRS argument.
    '''
    from .tasks import prepare_pair, metasync_collection
    from .utils import parse_pairs_args, WorkerQueue
    general, all_pairs, all_storages = ctx.obj['config']

    wq = WorkerQueue(max_workers)

    for pair_name, collections in parse_pairs_args(pairs, all_pairs):
        wq.put(functools.partial(prepare_pair, pair_name=pair_name,
                                 collections=collections,
                                 general=general, all_pairs=all_pairs,
                                 all_storages=all_storages,
                                 callback=metasync_collection))
        wq.spawn_worker()

    wq.join()


@app.command()
@click.argument('pairs', nargs=-1)
@max_workers_option
@catch_errors
def discover(pairs, max_workers):
    '''
    Refresh collection cache for the given pairs.
    '''
    from .tasks import discover_collections
    from .utils import WorkerQueue
    general, all_pairs, all_storages = ctx.obj['config']
    wq = WorkerQueue(max_workers)

    for pair in (pairs or all_pairs):
        try:
            name_a, name_b, pair_options = all_pairs[pair]
        except KeyError:
            raise CliError('Pair not found: {}\n'
                           'These are the pairs found: {}'
                           .format(pair, list(all_pairs)))

        wq.put(functools.partial(
            discover_collections,
            status_path=general['status_path'], name_a=name_a, name_b=name_b,
            pair_name=pair, config_a=all_storages[name_a],
            config_b=all_storages[name_b], pair_options=pair_options,
            skip_cache=True
        ))
        wq.spawn_worker()

    wq.join()


@app.command()
@click.argument('collection')
@catch_errors
def repair(collection):
    '''
    Repair a given collection.

    Runs a few checks on the collection and applies some fixes to individual
    items that may improve general stability, also with other CalDAV/CardDAV
    clients. In particular, if you encounter URL-encoding-related issues with
    other clients, this command might help.

    Example: `vdirsyncer repair calendars_local/foo` repairs the `foo`
    collection of the `calendars_local` storage.
    '''
    from .tasks import repair_collection
    general, all_pairs, all_storages = ctx.obj['config']

    cli_logger.warning('This operation will take a very long time.')
    cli_logger.warning('It\'s recommended to turn off other client\'s '
                       'synchronization features.')
    click.confirm('Do you want to continue?', abort=True)
    repair_collection(general, all_pairs, all_storages, collection)

# Not sure if useful. I originally wanted it because:
# * my password manager has a timeout for caching the master password
# * when calling vdirsyncer in a cronjob, the master password prompt would
#   randomly pop up
# So I planned on piping a FIFO to vdirsyncer, and writing to that FIFO from a
# cronjob.

try:
    import click_repl
    click_repl.register_repl(app)
except ImportError:
    pass
