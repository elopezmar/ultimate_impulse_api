from flask_restful import Resource, request

from models.users.user import User
from resources.utils import handle_request


class UserVerifyResource(Resource):
    @handle_request()
    def put(self):
        user = User(id=request.args['id']).get()
        user.verify()
        return {'message': 'User verified.'}, 200
