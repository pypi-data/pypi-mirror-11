"""core\__init__.py: This file initializes the core Blueprint."""

__author__ = 'dan'

from flask import Blueprint

core = Blueprint('core', __name__)

from . import views
