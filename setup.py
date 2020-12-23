#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script for the idmtools_git_tags"""
import sys

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

# Load our Requirements files
extra_require_files = dict()
for file_prefix in ['', 'dev_', 'build_']:
    filename = f'{file_prefix}requirements'
    with open(f'{filename}.txt') as requirements_file:
        fk = file_prefix.strip("_") if file_prefix else filename
        extra_require_files[fk] = [r for r in requirements_file.read().split("\n") if not r.startswith("--")]

extras = dict(
    test=extra_require_files['build'] + extra_require_files['dev'],
    dev=extra_require_files['build'] + extra_require_files['dev'],
    build=extra_require_files['build'],
    packaging=extra_require_files['build']
)

# TODO review
authors = [
    ("Clinton Collins", "ccollins@idmod.org"),
]

setup(
    author=[author[0] for author in authors],
    author_email=[author[1] for author in authors],
    classifiers=[
        'idmtools :: plugins :: general',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description="Add Git Info as tags to idmtools entities automatically",
    install_requires=extra_require_files['requirements'],
    long_description=readme,
    include_package_data=True,
    keywords='modeling, IDM',
    name='idmtools_git_tags',
    packages=find_packages(),
    setup_requires=[],
    python_requires='>=3.6.*, !=3.7.0, !=3.7.1, !=3.7.2',
    test_suite='tests',
    extras_require=extras,
    version='0.0.1.dev',
    entry_points=dict(
        idmtools_hooks=["idmtools_add_git_tag = idmtools_git_tags.git_info"]
    )
)