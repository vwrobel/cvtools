#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='scopethis_cvtools',
    version='0.1.0',
    description="CV tools to spot and track objects in a video",
    long_description=readme + '\n\n' + history,
    author="Valerian Wrobel",
    author_email='valerian.wrobel@gmail.com',
    url='https://github.com/vwrobel/scopethis_cvtools',
    packages=[
        'scopethis_cvtools',
    ],
    package_dir={'scopethis_cvtools':
                 'scopethis_cvtools'},
    entry_points={
        'console_scripts': [
            'scopethis_cvtools=scopethis_cvtools.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='scopethis_cvtools',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
