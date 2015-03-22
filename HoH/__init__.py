from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.sqlalchemy import SQLAlchemy

DEBUG = True
SECRET_KEY = 'hfd45t64,u-hg1h2fd5(ujet(-('
SQLALCHEMY_DATABASE_URI = 'sqlite:///storage/db.sqlite'
SQLALCHEMY_RECORD_QUERIES = True
SESSION_COOKIE_NAME = 'hoh'

app = Flask(__name__)
app.config.from_object(__name__)
toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)

from HoH.models.Account import Account
from HoH.models.AccountRegion import AccountRegion
from HoH.models.HeroHistory import HeroHistory
from HoH.models.Hero import Hero
from HoH.models.HeroClass import HeroClass

import HoH.filters
import HoH.routes