from flask_restful import Resource, request

from models.exceptions import BusinessError
from models.users.user import User


class UserVerifyResource(Resource):
    def put(self):
        try:
            User(id=request.args['id']).verify()
            return {'message': 'User verified.'}, 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message
