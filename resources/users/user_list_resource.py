from flask_restful import Resource

from models.users.user_list import UserList
from schemas.users.user_list_schema import UserListSchema
from resources.utils import handle_request


class UserListResource(Resource):
    @handle_request()
    def get(self):
        schema = UserListSchema()
        users = UserList().get()
        return schema.dump(users.to_dict('users')), 200
