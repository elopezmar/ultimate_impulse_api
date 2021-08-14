from flask_restful import Resource

from models.exceptions import BusinessError
from models.users.user_list import UserList
from schemas.users.user_list_schema import UserListSchema


class UserListResource(Resource):
    def get(self):
        try:
            schema = UserListSchema()
            users = UserList.get()
            return schema.dump(users.to_dict()), 200
        except BusinessError as err:
            return err.message
