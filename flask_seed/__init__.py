# -*- coding: utf-8 -*-

"""
    flaskext.flask-seed
    ---------------

    Flask extension for SQLAlchemy Seeding

    :copyright: (c) by Luke Smith.
    :license: MIT license , see LICENSE for more details.
"""

from flask_seed.commands import Seed
from flask_seed.ext import FlaskSeed

__all__ = ['Seed', 'FlaskSeed']

__author__ = """Luke Smith"""
__email__ = 'lsmith@zenoscave.com'
__version__ = '0.2.1'
