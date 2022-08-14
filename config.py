from distutils.debug import DEBUG
import os
from dotenv import load_dotenv

#Load the environment variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

#Define base object for configuration values
class BaseConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(12).hex() #cryptographic key for generating signatures or tokens
    SECURITY_PASSWORD_SALT = 'none'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    #Disable alerts to the app each time changes are made in the DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Log all executed queries if True
    SQLALCHEMY_ECHO = True

class DevConfig(BaseConfig):
    #Development specific config
    DEBUG = True

class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ECHO = False

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

app_config = {
    'development': DevConfig,
    'production': ProdConfig,
    'testing': TestingConfig
}
