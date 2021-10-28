from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.users.user import User
from schemas.users.user_schema import UserSchema
from resources.utils import get_requestor, handle_errors


class UserResource(Resource):
    @jwt_required(optional=True)
    @handle_errors()
    def post(self):
        schema = UserSchema(partial=('id',))
        data = schema.load(request.get_json())
        user = User().from_dict(data)
        user.set(get_requestor())
        return schema.dump(user.to_dict()), 201

    @handle_errors()
    def get(self):
        schema = UserSchema()
        user = User(id=request.args['id']).get()
        return schema.dump(user.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def put(self):
        schema = UserSchema(
            partial=('password', 'username', 'email'), 
            only=('id', 'old_password', 'new_password', 'username', 'profile')
        )
        data = schema.load(request.get_json())
        user = User().from_dict(data)
        user.update(get_requestor())
        return {'message': 'User updated.'}, 200

    @jwt_required()
    @handle_errors()
    def delete(self):
        schema = UserSchema(
            partial=('password', 'username', 'email'),
            only=('id',)
        )
        data = schema.load(request.get_json())
        user = User().from_dict(data)
        user.delete(get_requestor())
        return {'message': 'User deleted.'}, 200
