from flask import Blueprint
from flask_restful import Api

from resources.users.user_resource import UserResource
from resources.users.user_list_resource import UserListResource
from resources.users.user_login_resource import UserLoginResource
from resources.users.user_verify_resource import UserVerifyResource

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint)

api.add_resource(UserResource, '/user')
api.add_resource(UserListResource, '/users')
api.add_resource(UserLoginResource, '/user/login')
api.add_resource(UserVerifyResource, '/user/verify')
