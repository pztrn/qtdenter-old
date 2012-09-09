#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
from distutils.core import setup
import distutils.command.install_lib
import os

setup(name='qtdenter',
    version='0.1',
    description='Identi.ca/Status.Net client written in python and pyqt',
    author='Stanislav N. aka pztrn',
    author_email='pztrn@pztrn.ru',
    url='http://github.com/pztrn/qtdenter',
    packages=['qtdenter', 'qtdenter.ui', 'qtdenter.lib', 'qtdenter.identiparse', 'qtdenter.ui.imgs'],
    requires=["pyqt"],
    package_dir={'qtdenter': 'src'},
    data_files=[ ("bin", ["src/qtdenter"]), ("share/pixmaps", ["src/qtdenter.png"]), ("share/applications", ["src/qtdenter.desktop"]),
      ],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: X11 Applications :: Qt',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 2 :: Only',
      'Topic :: Communications :: Chat',
      ],
)
