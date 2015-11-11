#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found")
    read_md = lambda f: open(f, 'r').read()


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

try:
    readme = read_md('README.md')
except:
    readme = ""
try:
    changelog = read_md('CHANGELOG.md')
except:
    changelog = ""

setup(
    name='awg',
    version='0.1.1',
    description='automatic web generator',
    long_description=readme+'\n\n'+changelog,
    author='Alberto Galera Jimenez',
    author_email='galerajimenez@gmail.com',
    url='https://github.com/kianxineki/automatic_web_generator',
    py_modules=['awg'],
    include_package_data=True,
    install_requires=['requests','jinja2'],
    packages=['awg'],
    package_dir={'awg': 'awg-data'},
    package_data={'awg': ['awg-data/main.css', 'data/settings.json'],
                  'awg': ['awg-data/default_template/header.tpl',
                          'awg-data/default_template/index.tpl',
                          'awg-data/default_template/repo.tpl',
                          'awg-data/default_template/footer.tpl']},
    license="GPL",
    zip_safe=False,
    keywords='awg',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    entry_points={
        'console_scripts': [
            'awg = awg:generate'
        ]
    },
)
