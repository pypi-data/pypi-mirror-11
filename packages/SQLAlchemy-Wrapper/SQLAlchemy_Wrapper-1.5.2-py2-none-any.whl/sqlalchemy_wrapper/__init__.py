# coding=utf-8
"""
    ==================
    SQLAlchemy-Wrapper
    ==================

    A friendly wrapper for SQLAlchemy.

    :copyright: 2012-2015 by `Juan-Pablo Scaletti <http://jpscaletti.com>`_.
    :copyright: 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.

"""
from .main import SQLAlchemy, BaseQuery, Model  # noqa
from .paginator import Paginator, sanitize_page_number  # noqa
from .helpers import get_debug_queries  # noqa

__version__ = '1.5.2'
