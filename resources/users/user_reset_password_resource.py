from flask_restful import Resource, request

from models.users.user import User
from resources.utils import handle_request


class UserResetPasswordResource(Resource):
    @handle_request()
    def put(self):
        User.reset_password(request.args['email'])
        return {'message': 'Password reseted.'}, 200
