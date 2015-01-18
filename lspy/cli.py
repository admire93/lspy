""" :mod:`lspy.cli` --- command line interface for lspy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from functools import reduce
from itertools import chain

import click

from .dig import listing_informs, recursive_listing_informs
from .represent import find_represent
from .filter import find_filters
from .sort import find_sort

__all__ = 'cli', 'apply_funcs',

def apply_funcs(funcs, data):
    """Apply all functions in ``funcs`` .

    :param list funcs: a list of functions contains filters, represent and sort
    :param data: a list of :class:`lspy.dig.Inform` .

    :return: result of funcs
    """
    return reduce(lambda x, y: y(x), funcs, data)


@click.command()
@click.argument('path', default='.')
@click.option('--all', 'all_', default=False, is_flag=True,
              help='Include directory entries whose names begin '
                   'with a dot (.).')
@click.option('--long', 'long_', default=False, is_flag=True,
              help='List in long format.')
@click.option('--time', 'time_', default=False, is_flag=True,
              help='sort by modification time.')
@click.option('--changed', default=False, is_flag=True,
              help='with --long --time: sort by, and show, ctime '
                   'with --long: show ctime and  sort  by  name '
                   'otherwise: sort by ctime')
@click.option('--accessed', default=False, is_flag=True,
              help='with --long --time: sort by, and show, atime '
                   'with --long: show atime and  sort  by  name '
                   'otherwise: sort by atime')
@click.option('--reverse', default=False, is_flag=True,
              help='reverse order while sorting')
@click.option('--size', default=False, is_flag=True,
              help='sort by file size')
@click.option('--recursive', default=False, is_flag=True,
              help='list subdirectories recursively')
@click.option('--human', default=False, is_flag=True,
              help='with -l, print sizes in human readable format '
                   '(e.g., 1K 234M 2G)')
def cli(path, all_, long_, time_, changed, reverse, accessed, size, recursive,
        human):
    """Command Line Interface for lspy.

    .. sourcode::

       --all        Include directory entries whose names begin with a dot (.).
       --long       List in long format.
       --time       sort by modification time.
       --changed    with --long --time: sort by, and show, ctime with --long: show
                    ctime and  sort  by  name otherwise: sort by ctime
       --accessed   with --long --time: sort by, and show, atime with --long: show
                    atime and  sort  by  name otherwise: sort by atime
       --reverse    reverse order while sorting
       --size       sort by file size
       --recursive  list subdirectories recursively
       --human      with -l, print sizes in human readable format (e.g., 1K 234M
                    2G)
       --help       Show this message and exit.
    """
    funcs = list(chain(
        find_sort(time_=time_, changed=changed, long_=long_,
                  accessed=accessed, reverse=reverse, size=size),
        find_filters(all_=all_),
        find_represent(long_=long_, changed=changed, accessed=accessed,
                       human=human)
    ))
    if recursive:
        recursive_infos = recursive_listing_informs(path)
        for root, infos in recursive_infos.items():
            if not all_ and root.startswith('./.'):
                continue
            print('\n{}'.format(root))
            for f in apply_funcs(funcs, infos):
                click.echo(f)
    else:
        infos = listing_informs(path)
        for f in apply_funcs(funcs, infos):
            click.echo(f)
