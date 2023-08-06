# Authors:
#     Christian Heimes <cheimes@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright (C) 2015 Red Hat, Inc.
# All rights reserved.
#
"""

$ sudo yum install python-wheel python-setuptools
$ python setup.py release

"""

import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(specfile='../../../specs/pki-core.spec'):
    version_re = re.compile('^Version:\s*(\d+\.\d+\.\d+)')
    release_re = re.compile('^Release:.*?([0-9\.]+)')
    version = release = None
    with open(specfile) as f:
        for line in f:
            if version is None:
                match = version_re.match(line)
                if match is not None:
                    version = match.group(1)
            if release is None:
                match = release_re.match(line)
                if match is not None:
                    release = match.group(1)
            if version is not None and release is not None:
                break
    if version is None or release is None:
        raise ValueError(version, release)
    print(version, release)
    return "%s.%s" % (version, release)

VERSION = get_version()

setup(
    author='Dogtag Certificate System Team',
    author_email='pki-devel@redhat.com',
    name='dogtag-pki',
    version=VERSION,
    description='Dogtag Certificate System',
    long_description="""\
The Dogtag Certificate System is an enterprise-class open source
Certificate Authority (CA). It is a full-featured system, and has been
hardened by real-world deployments. It supports all aspects of certificate
lifecycle management, including key archival, OCSP and smartcard management,
and much more. The Dogtag Certificate System can be downloaded for free
and set up in less than an hour.""",
    license='GPL',
    keywords='pki x509 cert certificate',
    url='http://pki.fedoraproject.org/',
    packages=['pki'],
    requirements=['python-nss', 'six'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Topic :: Security :: Cryptography',
    ],
)

