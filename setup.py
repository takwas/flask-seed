#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'flask',
    'flask_script',
    'SQLAlchemy'
]

test_requirements = [
    'tox',
    'flake8',
    'pytest',
    'pytest-cov',
    'flask_sqlalchemy'
]

setup(
    name='flask_seed',
    version='0.1.0',
    description="Flask extension for SQLAlchemy Seeding",
    long_description=readme + '\n\n' + history,
    author="Luke Smith",
    author_email='lsmith@zenoscave.com',
    url='https://github.com/LSmith-Zenoscave/flask-seed',
    packages=[
        'flask_seed',
    ],
    entry_points={
        'flask.commands': [
            'seed=flask_seed:Seed'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='flask_seed',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
