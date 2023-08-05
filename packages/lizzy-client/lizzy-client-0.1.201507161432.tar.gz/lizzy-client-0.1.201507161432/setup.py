#!/usr/bin/env python3
"""
Copyright 2015 Zalando SE

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific
 language governing permissions and limitations under the License.
"""

from setuptools import setup, find_packages
import datetime

version = "0.1.{:%Y%m%d%H%M}".format(datetime.datetime.now())

setup(
    name='lizzy-client',
    packages=find_packages(),
    version=version,
    description='Lizzy-client',
    author='Zalando SE',
    url='https://github.com/zalando/lizzy-client',
    license='Apache License Version 2.0',
    install_requires=['click', 'clickclick>=0.10', 'requests', 'pyyaml', 'python-dateutil'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    long_description='Lizzy-client',
    entry_points={'console_scripts': ['lizzy = lizzy_client:cli']},
)
