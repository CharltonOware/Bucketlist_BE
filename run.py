import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from config import app_config
from app.models import db
from app.resources import UserRegistration, UserLogin, BucketListAPI, BucketListItemAPI, AllUsers

#use the config from the environment file as default
config_name = os.getenv('FLASK_ENV')
app = Flask(__name__)
#configure app from an object in config file
app.config.from_object(app_config['development'])
#introduce app secret key
app.config['SECRET_KEY'] = os.urandom(12).hex()
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
docs = FlaskApiSpec(app)

#Enable CORS support
CORS(app)
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS")
    return response

#Register endpoint inside our application
app.add_url_rule('/registration',view_func=UserRegistration.as_view('registration'))
app.add_url_rule('/login', view_func=UserLogin.as_view('login'))
app.add_url_rule('/users', view_func=AllUsers.as_view('users'))
app.add_url_rule('/bucketlist', view_func=BucketListAPI.as_view('bucketlist'))
app.add_url_rule('/bucketlist/<int:id>', view_func=BucketListItemAPI.as_view('bucketlistitem'))

docs.register(UserRegistration, endpoint='registration')
docs.register(UserLogin, endpoint='login')
docs.register(BucketListAPI, endpoint='bucketlist')
docs.register(BucketListItemAPI, endpoint='bucketlistitem')