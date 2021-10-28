from flask_restful import Resource, request

from models.users.user import User
from resources.utils import handle_errors


class UserVerifyResource(Resource):
    @handle_errors()
    def put(self):
        User(id=request.args['id']).verify()
        return {'message': 'User verified.'}, 200
