#!/usr/bin/env python

from wagtailplus import __version__


try:
    from setuptools import (
        setup,
        find_packages
    )
except ImportError:
    from distutils.core import setup


# Hack to prevent "TypeError: 'NoneType' object is not callable" error
# in multiprocessing/util.py _exit_function when setup.py exits
# (see http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass

install_requires = [
    "wagtail==1.0",
]

setup(
    name                    = 'wagtailplus',
    packages                = find_packages(),
    version                 = __version__,
    description             = 'Modular add-ons for Wagtail CMS',
    author                  = 'Ryan Foster',
    author_email            = 'rfosterslo@gmail.com',
    url                     = 'https://github.com/rfosterslo/wagtailplus',
    download_url            = 'https://github.com/rfosterslo/wagtailplus/archive/v0.2.3.tar.gz',
    keywords                = ['django', 'wagtail', 'cms'],
    install_requires        = install_requires,
)
