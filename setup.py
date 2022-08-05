#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='c3-web-query',
    packages=find_packages(),
    version='0.0.1',
    description='To query or push C3 service.',
    author='Taihsiang Ho (tai271828)',
    author_email='taihsiang.ho@canonical.com',
    url='https://github.com/tai271828/c3-web-query',
    download_url='git@github.com:tai271828/c3-web-query.git',
    keywords=['c3'],
    entry_points={
        'console_scripts': [
            'c3-cli=c3.commands.c3_cli:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python",
    ],
    data_files=[
        ('c3/data', ['c3/data/default.ini'])
    ],
    zip_safe=False
)
