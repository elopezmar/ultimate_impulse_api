from flask_restful import Resource, request
from marshmallow import ValidationError

from models.exceptions import BusinessError
from models.users.user import User
from schemas.users.user_schema import UserSchema

class UserLoginResource(Resource):
    def post(self):
        try:
            schema = UserSchema(partial=('id', 'username'))
            data = schema.load(request.get_json())
            access_token, user = User().from_dict(data).login()

            return {
                'access_token': access_token,
                'user': schema.dump(user.to_dict())
            }, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message
