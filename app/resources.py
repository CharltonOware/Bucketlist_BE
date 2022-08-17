from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs, MethodResource
from models import db, UserModel,BucketList
from app.schema import UserResponseSchema, ItemResponseSchema


#Define UserRegistration endpoint
class UserRegistration(MethodResource,Resource):
    #Define fields
    @use_kwargs(UserResponseSchema(), location='json')
    #Encode user data
    @marshal_with(UserResponseSchema(), code=201)
    def post(self,**kwargs):
        #Abort if the user already exists in DB
        email = kwargs.get('email')
        if UserModel.find_by_email(email):
            return {'message': f'User {email} already exists'}, 400
        
        #Create new user
        new_user = UserModel(**kwargs)
        try:
            new_user.save_to_db()
            return {'message': f'New user {new_user.email} created'}
        except:
            return {'message': 'Something went wrong'}, 500