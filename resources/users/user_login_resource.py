from flask_restful import Resource, request

from models.users.user import User
from schemas.users.user_schema import UserSchema
from resources.utils import handle_errors


class UserLoginResource(Resource):
    @handle_errors()
    def post(self):
        schema = UserSchema(partial=('id', 'username'))
        data = schema.load(request.get_json())
        access_token, user = User().from_dict(data).login()

        return {
            'access_token': access_token,
            'user': schema.dump(user.to_dict())
        }, 200
