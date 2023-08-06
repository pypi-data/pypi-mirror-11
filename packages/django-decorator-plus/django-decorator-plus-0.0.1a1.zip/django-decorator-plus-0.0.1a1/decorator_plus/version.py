#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provide PEP 440 Compliant Versioning Scheme."""

from __future__ import print_function, unicode_literals

from datetime import datetime
from subprocess import PIPE, Popen


DEV = 'dev'
ALPHA = 'a'
BETA = 'b'
RC = 'rc'  # Release Candidate
FINAL = ''  # Release
POST = 'post'
SEPARATOR = '.'


# PEP 440 Compliant Semantic Versioning
# major, minor, micro, label/type, label/type number
VERSION = (0, 0, 1, ALPHA, 1)


def get_git_changeset():
    """Get git identifier; taken from Django project."""
    git_log = Popen(
        'git log --pretty=format:%ct --quiet -1 HEAD',
        stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
    timestamp = git_log.communicate()[0]
    try:
        timestamp = datetime.utcfromtimestamp(int(timestamp))
    except ValueError:
        return None
    return timestamp.strftime('%Y%m%d%H%M%S')


def get_version(version_tuple):
    """Convert 4-tuple into a PEP 440 compliant string."""
    if version_tuple[3] == FINAL and version_tuple[4] != 0:
        raise Exception(
            'Project version number misconfigured:\n'
            '   version may not be final and have segment number.')

    if version_tuple[3] not in (DEV, FINAL) and version_tuple[4] == 0:
        raise Exception(
            'Project version number misconfigured:\n'
            '   version must have segment number.')

    if version_tuple[3] == DEV:
        segment_num = get_git_changeset()
    else:
        segment_num = str(abs(version_tuple[4]))

    # X.X.X
    sem_ver = ".".join([
        str(abs(int(number)))
        for number in version_tuple[:3]
    ])

    if version_tuple[3] != FINAL:
        if version_tuple[3] in (ALPHA, BETA, RC):
            sem_ver = "%s%s%s" % (sem_ver, version_tuple[3], segment_num)
        elif version_tuple[3] in (DEV, POST):
            sem_ver = "%s%s%s%s" % (
                sem_ver, SEPARATOR, version_tuple[3], segment_num)
        else:
            raise Exception(
                'Project version number misconfigured:\n'
                '   Unrecognized release type')

    return sem_ver


__version__ = get_version(VERSION)
