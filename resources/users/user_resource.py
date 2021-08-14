from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from marshmallow import ValidationError

from models.exceptions import BusinessError
from models.users.user import User
from schemas.users.user_schema import UserSchema
from resources.utils import get_requestor


class UserResource(Resource):
    @jwt_required(optional=True)
    def post(self):
        try:
            schema = UserSchema(partial=('id',))
            data = schema.load(request.get_json())
            user = User().from_dict(data)
            user.set(get_requestor())
            return schema.dump(user.to_dict()), 201
        except ValidationError as err:
            return err.messages 
        except BusinessError as err:
            return err.message

    def get(self):
        try:
            schema = UserSchema()
            user = User(id=request.args['id']).get()
            return schema.dump(user.to_dict()), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message

    @jwt_required()
    def put(self):
        try:
            schema = UserSchema(
                partial=('password', 'username', 'email'), 
                only=('id', 'old_password', 'new_password', 'username', 'profile')
            )
            data = schema.load(request.get_json())
            user = User().from_dict(data)
            user.update(get_requestor())
            return {'message': 'User updated.'}, 200
        except ValidationError as err:
            return err.messages 
        except BusinessError as err:
            return err.message

    @jwt_required()
    def delete(self):
        try:
            schema = UserSchema(
                partial=('password', 'username', 'email'),
                only=('id',)
            )
            data = schema.load(request.get_json())
            user = User().from_dict(data)
            user.delete(get_requestor())
            return {'message': 'User deleted.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message
