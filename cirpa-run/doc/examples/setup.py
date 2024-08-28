# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='examples',
    version='1.0.0a1',
    description='Example code for cirpa-run',
    long_description='Example code for cirpa-run',
    author='Hakan Bengtsen',
    author_email='hakan.bengtsen@ericsson.se',
    url='https://gerrit.ericsson.se/#/admin/projects/CBA/cirpa',
    license="Ericsson...",
    packages=find_packages(exclude=('tests', 'docs'))
)
