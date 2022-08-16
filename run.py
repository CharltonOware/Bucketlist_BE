import os
from flask import Flask
from flask_migrate import Migrate

from config import app_config
from app.models import db, UserModel, BucketList

#use the config from the environment file as default
config_name = os.getenv('FLASK_ENV')
app = Flask(__name__)
#configure app from an object in config file
app.config.from_object(app_config['development'])

db.init_app(app)

migrate = Migrate(app, db)


