import re

import semver
from invoke import run

from ..settings import config
from .logs import evaluate_version_bump  # noqa

from .parser_angular import parse_commit_message as angular_parser  # noqa isort:skip


def get_current_version():
    """
    Finds the current version of the package in the current working directory.

    :return: A string with the version number.
    """
    return run('python setup.py --version', hide=True).stdout.strip()


def get_new_version(current_version, level_bump):
    """
    Calculates the next version based on the given bump level with semver.

    :param current_version: The version the package has now.
    :param level_bump: The level of the version number that should be bumped. Should be a `'major'`,
                       `'minor'` or `'patch'`.
    :return: A string with the next version number.
    """
    if not level_bump:
        return current_version
    return getattr(semver, 'bump_{0}'.format(level_bump))(current_version)


def set_new_version(new_version):
    """
    Replaces the version number in the correct place and writes the changed file to disk.

    :param new_version: The new version number as a string.
    :return: `True` if it succeeded.
    """
    filename, variable = config.get('semantic_release', 'version_variable').split(':')
    variable = variable.strip()
    with open(filename, mode='r') as fr:
        content = fr.read()

    content = re.sub(
        r'{} ?= ?["\']\d+\.\d+(?:\.\d+)?["\']'.format(variable),
        '{} = \'{}\''.format(variable, new_version),
        content
    )

    with open(filename, mode='w') as fw:
        fw.write(content)
    return True
