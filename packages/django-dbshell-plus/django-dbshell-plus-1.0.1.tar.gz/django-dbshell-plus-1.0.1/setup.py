#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from setuptools import setup, find_packages

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def read_reqs(name):
    with open(os.path.join(os.path.dirname(__file__), name)) as f:
        return [line for line in f.read().split('\n') if line and not line.strip().startswith('#')]


def read_version():
    with open(os.path.join('lib', 'django_dbshell_plus', '__init__.py')) as f:
        m = re.search(r'''__version__\s*=\s*['"]([^'"]*)['"]''', f.read())
        if m:
            return m.group(1)
        raise ValueError("couldn't find version")


# NB: _don't_ add namespace_packages to setup(), it'll break
#     everything using imp.find_module
setup(
    name='django-dbshell-plus',
    version=read_version(),
    description='A dbshell_plus management command for Django that selects pgcli or mycli when available.',
    long_description=readme + '\n\n' + history,
    author='Simon Percivall',
    author_email='percivall@gmail.com',
    url='https://github.com/simonpercivall/django-dbshell-plus',
    packages=find_packages('lib'),
    package_dir={'': 'lib'},
    include_package_data=True,
    install_requires=read_reqs('requirements.txt'),
    license="BSD",
    zip_safe=False,
    keywords='django-dbshell-plus',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
