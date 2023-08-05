# -*- coding: utf-8 -*-
"""
Python library for interacting with the T1 API. Uses third-party module Requests
(http://docs.python-requests.org/en/latest/) to get and post data, and ElementTree
to parse it.
"""

from __future__ import absolute_import
from .utils import filters
from .service import T1, T1Service
from . import errors

__author__ = 'Prasanna Swaminathan'
__copyright__ = 'Copyright 2015, MediaMath'
__license__ = 'BSD'
__version__ = '1.0.3a1'
__maintainer__ = 'Prasanna Swaminathan'
__email__ = 'prasanna@mediamath.com'
__status__ = 'Development'
__all__ = ['T1', 'T1Service', 'filters', 'errors']
