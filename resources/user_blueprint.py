from flask import Blueprint
from flask.app import Flask
from flask_restful import Api

from resources.users.user_resource import UserResource
from resources.users.user_list_resource import UserListResource
from resources.users.user_login_resource import UserLoginResource
from resources.users.user_verify_resource import UserVerifyResource
from resources.users.user_reset_password_resource import UserResetPasswordResource
from resources.users.user_purchase_list_resource import UserPurchaseListResource

user_blueprint = Blueprint('user', __name__)
api = Api(user_blueprint, errors=Flask.errorhandler)

api.add_resource(UserResource, '/user')
api.add_resource(UserListResource, '/users')
api.add_resource(UserLoginResource, '/user/login')
api.add_resource(UserVerifyResource, '/user/verify')
api.add_resource(UserResetPasswordResource, '/user/reset-password')
api.add_resource(UserPurchaseListResource, '/user/<string:user_id>/purchases')
