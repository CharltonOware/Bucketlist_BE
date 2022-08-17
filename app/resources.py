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

#Define UserLogin endpoint
class UserLogin(MethodResource, Resource):
    @use_kwargs(UserResponseSchema, location='json')
    @marshal_with(UserResponseSchema(), code=200)
    def post(self, **kwargs):
        email = kwargs.get('email')
        current_user = UserModel.find_by_email(email)

        #Abort if credentials don't exist in the DB
        if not current_user:
            return {'message': f'User {email} doesn\'t exist'}, 400
        if current_user.verify_password(kwargs['password']):
            return {'message': f'Logged in as {current_user.email}'}, 200

#Define view for all user
class AllUsers(MethodResource, Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()