from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey

db = SQLAlchemy()

#Define Usermodel
class UserModel(db.Model):
    '''Table to store user information.'''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    bucketlists = db.relationship(
        'BucketList', backref='user',lazy=True, passive_deletes=True)

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

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'email': x.email,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), cls.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': f'{num_rows_deleted} row(s) deleted'}
        except:
            return {'message': 'Something went wrong'}

    def __repr__(self):
        return f"<UserModel: {self.email}>"


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
    created_by = db.Column(db.Integer, ForeignKey('users.id',ondelete='CASCADE'))

    #Initialize an instance of BucketList model
    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        #Return all bucketlist items with names matching the search name
        return cls.query.order_by(cls.id).filter_by(cls.name.ilike('%{name}%')).first()

    @staticmethod
    def get_all(user_id):
        """This method gets all the bucketlists for a given user."""
        return BucketList.query.filter_by(created_by=user_id)

    def delete(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<BucketList: {self.name}>"
