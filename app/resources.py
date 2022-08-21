from flask.views import MethodView
from flask_apispec import marshal_with, use_kwargs, MethodResource, doc
from app.models import UserModel,BucketList
from app.schema import UserResponseSchema, ItemResponseSchema


#Define UserRegistration endpoint
class UserRegistration(MethodResource,MethodView):
    #Document API endpoint
    #@doc(description='Register User API.',tags=['Register'],responses=None)
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
class UserLogin(MethodResource, MethodView):
    #@doc(description='Login User API.',tags=['Login'],responses=None)
    @use_kwargs(UserResponseSchema(), location='json')
    @marshal_with(UserResponseSchema(), code=200)
    def post(self, **kwargs):
        email = kwargs.get('email')
        current_user = UserModel.find_by_email(email)

        #Abort if credentials don't exist in the DB
        if not current_user:
            return {'message': f'User {email} doesn\'t exist'}, 400
        if current_user.verify_password(kwargs['password']):
            return {'message': f'Logged in as {current_user.email}'}, 200

#Define view for all users
class AllUsers(MethodResource, MethodView):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()

#Define BucketListAPI resource for viewing and creating
class BucketListAPI(MethodResource, MethodView):
    #@doc(description='Get Bucketlist Items API.',tags=['Display Bucketlist'],responses=None)
    @marshal_with(ItemResponseSchema(many=True), code=200)
    def get(self):
        """Get all bucketlist items created by the current user."""
        bucketlist = BucketList.query.order_by(BucketList.id).all()
        return bucketlist
    
    #@doc(description='Create Bucketlist Item API.',tags=['Create Bucketlist item'],responses=None)
    @use_kwargs(ItemResponseSchema(), location='json')
    @marshal_with(ItemResponseSchema(), code=201)
    def post(self, **kwargs):
        name = kwargs['name']
        #Confirm name is in the request parameters
        if name:
            #Abort if provided bucketlist name already exists for this user in the DB
            if BucketList.find_by_name(name):
                return {'message': f'An item with the name {name} already exists.'}
            bucketlist = BucketList(name=name, created_by='Placeholder')
            try:
                bucketlist.save_to_db()
                return {'message': f'New item {name} created.'}
            except:
                return {'message': 'Something went wrong.'}
        else:
            return {'message': 'Please provide all required data.'}

#Define BucketListItemAPI that has show, update and delete capability implemented
class BucketListItemAPI(MethodResource, MethodView):
    """""" 
    #@doc(description='Get specific item API.',tags=['Display Bucketlist item'],responses=None)  
    @marshal_with(ItemResponseSchema, code=200)
    def get(self, id):
        """Get bucketlist item of the specified id."""
        item = BucketList.query.filter_by(id=id).first_or_none()
        if not item:
            return {'message': f'Item {item.name} doesn\'t exist'}, 400
        return item
    
    #@doc(description='Update specific item API.',tags=['Update Bucketlist item'],responses=None)
    @use_kwargs(ItemResponseSchema(), location='json')
    @marshal_with(ItemResponseSchema(), code=200)
    def patch(self, id, **kwargs):
        """Update the specified Bucketlist item."""
        item = BucketList.query.filter_by(id=id).first_or_none()
        item.name = kwargs['name']
        item.done = kwargs['done']
        item.save_to_db()

        return item

    #@doc(description='Delete item API.',tags=['Delete bucketlist item'],responses=None)
    def delete(self, id):
        """Delete the specified Bucketlist item."""
        item = BucketList.query.filter_by(id=id).first_or_none()
        if item:
            item.delete()
            return {'message': f'Item {item.id} deleted.'}, 204




