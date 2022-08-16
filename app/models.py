from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#Define Usermodel
class UserModel(db.Model):
    '''Table to store user information.'''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    bucketlists = db.relationship(
        'BucketList', backref='user',lazy='dynamic', order_by='BucketList.id', cascade="all, delete-orphan")

    #Initialize an instance of UserModel
    def __init__(self, email, password):
        self.email = email
        self.hash_password(password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #generate a password hash
    def hash_password(self, password):
        self.password = generate_password_hash(password)

    #Return True if user provided password matches the hash, otherwise return False
    def verify_password(self, password):
        return check_password_hash(self.password, password)

#Define BucketList Model
class BucketList(db.Model):
    '''Table to store our bucketlists.'''
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)
    created_by = db.column(db.Integer, db.ForeignKey("users.id"))

    #Initialize an instance of BucketList model
    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()