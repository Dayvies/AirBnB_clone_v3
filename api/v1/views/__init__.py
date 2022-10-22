#!/usr/bin/python3
"""Initialise"""

from flask import Flask, Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.states import *
from api.v1.views.index import *