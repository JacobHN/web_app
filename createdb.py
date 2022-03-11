from webapp import db
from webapp import create_app
from webapp.models import *

db.create_all(app=create_app())