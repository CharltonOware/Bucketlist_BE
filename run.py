import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import app_config
from app.models import db, UserModel, BucketList
from app import resources

#use the config from the environment file as default
config_name = os.getenv('FLASK_ENV')
app = Flask(__name__)
#configure app from an object in config file
app.config.from_object(app_config['development'])

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


#Register endpoint inside our application
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.BucketListAPI, '/bucketlist')
api.add_resource(resources.BucketListItemAPI, '/bucketlist/<int:id>')