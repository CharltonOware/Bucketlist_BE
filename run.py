import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from config import app_config
from app.models import db, UserModel, BucketList
from app import resources

#use the config from the environment file as default
config_name = os.getenv('FLASK_ENV')
app = Flask(__name__)
#configure app from an object in config file
app.config.from_object(app_config['development'])
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Bucketlist Project',
        version='1.0.0',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/', #URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/' #URI to access UI of API Doc
})

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
docs = FlaskApiSpec(app)

#Enable CORS support
CORS(app)
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS")
    return response

#Register endpoint inside our application
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.BucketListAPI, '/bucketlist')
api.add_resource(resources.BucketListItemAPI, '/bucketlist/<int:id>')

docs.register(resources.UserRegistration)
docs.register(resources.UserLogin)
docs.register(resources.BucketListAPI)
docs.register(resources.BucketListItemAPI)