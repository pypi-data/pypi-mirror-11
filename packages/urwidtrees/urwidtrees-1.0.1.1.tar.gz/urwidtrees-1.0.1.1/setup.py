#!/usr/bin/env python

from distutils.core import setup
import urwidtrees.version as v


setup(name='urwidtrees',
      version=v.__version__,
      description=v.__description__,
      author=v.__author__,
      author_email=v.__author_email__,
      url=v.__url__,
      license=v.__copyright__,
      packages=['urwidtrees'],
      requires=['urwid (>=1.1.0)'],
     )
