#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages

setup(
    name='crud_filters',
    packages=['CRUDFilters'],
    # packages=find_packages(exclude=['tests*']),
    version='0.1.6',
    description='django-crud-filters works with django-restframework to provide easily configurable role-based filtering for API endpoints.',
    author='Bellhops',
    author_email='tech@getbellhops.com',
    url='https://github.com/bellhops/django-crud-filters',
    download_url='https://github.com/bellhops/django-crud-filters/dist/crud_filters-0.1.6.tar.gz',
    keywords=['django', 'authorization', 'api', 'security'],
    classifiers=[],
    install_requires=['Django', 'djangorestframework', 'djangorestframework-expiring-authtoken', 'django-dynamic-fixture', 'Pillow'],
)
