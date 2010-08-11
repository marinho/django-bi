from distutils.command.install import INSTALL_SCHEMES
import os, sys

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup(
    name = 'django-bi',
    author = 'Marinho Brandao',
    author_email = 'marinho@gmail.com',
    license = 'GNU Lesser General Public License (LGPL)',
    packages = ['bi'],
    data_files = data_files,
)

