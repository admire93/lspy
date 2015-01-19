""" :mod:`lspy.dig` --- dig file to get information.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from collections import namedtuple, OrderedDict
from datetime import datetime
from grp import getgrgid
from pathlib import Path
from pwd import getpwuid

import os
import stat

__all__ = (
    'get_fileinfo',
    'Inform',
    'listing_informs',
    'recursive_listing_informs',
)

#: ``namedtuple`` that contains information of file or directory
Inform = namedtuple('Inform', ['permission', 'owner', 'size',
                               'is_dir', 'modified_at', 'accessed_at',
                               'changed_at', 'mode', 'name'])

def get_fileinfo(filename):
    """Return information ( permission, owner, ... ) of file or directory.

    :param str filename: a filename or directory that want to know.
    :return: information of file.
    :rtype: dict
    """
    path = Path(filename)
    if not path.exists():
        raise FileNotFoundError(
            'No such file or directory: {}'.format(filename))
    status = os.stat(filename)
    return Inform(
        name=path.name or filename,
        mode=status.st_mode,
        permission=stat.S_IMODE(status.st_mode),
        owner={
            'uid': status.st_uid,
            'gid': status.st_gid,
            'uname': getpwuid(status.st_uid).pw_name,
            'gname': getgrgid(status.st_gid).gr_name
        },
        size=status.st_size,
        is_dir=stat.S_ISDIR(status.st_mode),
        changed_at=datetime.fromtimestamp(status.st_ctime),
        modified_at=datetime.fromtimestamp(status.st_mtime),
        accessed_at=datetime.fromtimestamp(status.st_mtime),
    )


def recursive_listing_informs(path):
    """Recursively listing a files and directory.

    :param str path: path that want to listing.
    :return: a dictionary that key is a root path and value is list of `Inform`
    :rtype: :class:`OrderedDict`
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            'No such file or directory: {}'.format(path))
    result = OrderedDict()
    for root, dirs, files in os.walk(str(path)):
        result.setdefault(root, [])
        root_path = Path(root)
        for dir_ in dirs:
            result[root].append(get_fileinfo(str(root_path / dir_)))
        for file_ in files:
            result[root].append(get_fileinfo(str(root_path / file_)))
    return result


def listing_informs(path):
    """Listing a files and directory as a :class:`Inform` in ``path`` .

    :param str path: path that want to listing.
    :return: a list of :class:`Inform` .
    :rtype: list
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            'No such file or directory: {}'.format(path))
    result = [get_fileinfo('.'), get_fileinfo('..')]
    for root, dirs, files in os.walk(str(path)):
        root_path = Path(root)
        for dir_ in dirs:
            result.append(get_fileinfo(str(root_path / dir_)))
        for file_ in files:
            result.append(get_fileinfo(str(root_path / file_)))
        break
    return result
