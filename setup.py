# -*- coding: utf-8 -*-
"""setup.py"""

from setuptools import setup
from setuptools import find_packages


requires = []
with open('requirements.txt', 'w') as _file:
    _file.write('\n'.join(requires))

setup(
    name='django-graphql-jwt-demo',
    version='0.0.2',
    url='https://github.com/mtoshi/django-graphql-jwt-demo',
    author='mtoshi',
    author_email='mtoshi@outlook.com',
    description='Experimental app.',
    packages=find_packages(),
    install_requires=requires,
)
