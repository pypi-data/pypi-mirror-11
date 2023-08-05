# coding: utf-8
# flake8: noqa
"""
The package asynctest is built on top of the standard :mod:`unittest` module
and cuts down boilerplate code when testing libraries for :mod:`asyncio`.

Currently, asynctest only supports Python 3.4.

asynctest imports the standard unittest package, overrides some of its features
and adds new ones. A test author can import asynctest in place of
:mod:`unittest` safely.


asynctest is divided in submodules, but they are all imported at the top level,
so :class:`asynctest.case.TestCase` is equivalent to :class:`asynctest.TestCase`.
"""

import unittest
from unittest import *

# Shadows unittest with our enhanced classes
from .case import *
from .mock import *

# And load or own tools
from .helpers import *
from .selector import *

__all__ = unittest.__all__
