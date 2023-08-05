# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

name = 'onegov.ticket'
description = (
    'A simple ticketing system for OneGov.'
)
version = '0.0.4'


def get_long_description():
    readme = open('README.rst').read()
    history = open('HISTORY.rst').read()

    # cut the part before the description to avoid repetition on pypi
    readme = readme[readme.index(description) + len(description):]

    return '\n'.join((readme, history))


setup(
    name=name,
    version=version,
    description=description,
    long_description=get_long_description(),
    url='http://github.com/OneGov/onegov.ticket',
    author='Seantis GmbH',
    author_email='info@seantis.ch',
    license='GPLv2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=name.split('.')[:-1],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'onegov.core>=0.4.11',
        'onegov.user'
    ],
    extras_require=dict(
        test=[
            'coverage',
            'mock',
            'onegov.testing',
            'pytest',
        ],
    ),
    entry_points={
        'onegov': [
            'upgrade = onegov.ticket.upgrade'
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    ]
)
