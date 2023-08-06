#!/usr/bin/env python
'''
Please be aware, that `setup.py.in` is just a template.
Strings between `@` will be replaced with variables from
Makefile, see target `setup.py`

RELEASE will be replaced with `git describe`
SETUPLIB by default is `distutils.core`

To use `setuptools`, run `make ... setuplib=setuptools`
'''
import os
import sys
from distutils.core import setup

readme = open("README.md", "r")

# The goal of the following code is to have all the files
# in one bundle, but for Python2 install *only* Python2
# specific files. The reason is that Python3 code can
# cause SyntaxError being installed via Python2 -- even
# if it doesn't run. The exception is not fatal, but can
# be pretty confusing.
python2_only_files = ['./pyroute2/netns/process/base_p2.py']
python3_only_files = ['./pyroute2/netns/process/base_p3.py']


def cleanup(files):
    for name in files:
        try:
            os.unlink(name)
        except OSError:
            pass

# Run cleanup only if we're not called with proper keywords.
# Don't run cleanup on a git repository.
if (sys.argv[1] == 'primary'):
    sys.argv.pop(1)
else:
    if '.git' not in os.listdir('.'):
        if sys.version_info[0] == 2:
            cleanup(python3_only_files)

setup(name='pyroute2',
      version='0.3.14',
      description='Python Netlink library',
      author='Peter V. Saveliev',
      author_email='peter@svinota.eu',
      url='https://github.com/svinota/pyroute2',
      license='dual license GPLv2+ and Apache v2',
      packages=['pyroute2',
                'pyroute2.config',
                'pyroute2.dhcp',
                'pyroute2.ipdb',
                'pyroute2.netns',
                'pyroute2.netns.process',
                'pyroute2.netlink',
                'pyroute2.netlink.generic',
                'pyroute2.netlink.ipq',
                'pyroute2.netlink.nfnetlink',
                'pyroute2.netlink.rtnl',
                'pyroute2.netlink.taskstats',
                'pyroute2.netlink.nl80211',
                'pyroute2.protocols',
                'pyroute2.remote'],
      classifiers=['License :: OSI Approved :: GNU General Public ' +
                   'License v2 or later (GPLv2+)',
                   'License :: OSI Approved :: Apache Software License',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: ' +
                   'Python Modules',
                   'Operating System :: POSIX',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Development Status :: 4 - Beta'],
      long_description=readme.read())
