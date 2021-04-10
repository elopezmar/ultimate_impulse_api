from flask_restful import Resource, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from werkzeug.security import safe_str_cmp
from marshmallow import ValidationError

from schemas.user import UserSchema, UserUpdateSchema, BusinessError


class UserLogin(Resource):
    user_schema = UserSchema()

    def post(self):
        try:
            json_data = request.get_json()
            login = self.user_schema.load(json_data, partial=('id', 'username'))
            user = self.user_schema.read(user_email=login['email'], dump=False)
            if user.get('verified'):
                user_password = user['password'].encode('utf-8')
                login_password = login['password'].encode('utf-8')
                if safe_str_cmp(user_password, login_password):
                    access_token = create_access_token(identity=user['id'])
                    return {'access_token': access_token}
                raise BusinessError('Invalid email or password.', 400)
            raise BusinessError('User not verified.', 400)
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message


class UserVerify(Resource):
    # TODO Es necesario agregar mas seguridad a la verificación del usuario?
    user_schema = UserUpdateSchema()

    def post(self):
        try:
            args = request.args
            user_id = args['id']
            user = {'verified': True}
            self.user_schema.update(user_id, user, validate_privileges=False)
            return {'message': 'User verified.'}, 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message


class User(Resource):
    user_schema = UserSchema(exclude=('verified',))

    def post(self):
        try:
            json_data = request.get_json()
            user = self.user_schema.load(json_data, partial=('id',))
            if self.user_schema.read(user_email=user['email'], raise_errors=False):
                raise BusinessError('Email already exists.', 400)
            if self.user_schema.read(user_username=user['username'], raise_errors=False):
                raise BusinessError('Username already exists.', 400)
            return self.user_schema.create(user), 201
        except ValidationError as err:
            return err.messages 
        except BusinessError as err:
            return err.message

    @jwt_required()
    def get(self):
        try:
            args = request.args
            user_id = args['id']
            return self.user_schema.read(user_id=user_id), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message

    @jwt_required()
    def put(self):
        user_schema = UserUpdateSchema(
            only=('old_password', 'new_password', 'username', 'profile')
        )
        try:
            args = request.args
            user_id = args['id']
            json_data = request.get_json()
            user = user_schema.load(json_data, partial=('id', 'password', 'username'))
            user_schema.update(user_id, user)
            return {'message': 'User updated.'}, 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except ValidationError as err:
            return err.messages 
        except BusinessError as err:
            return err.message

    @jwt_required()
    def delete(self):
        try:
            args = request.args
            user_id = args['id']
            self.user_schema.delete(user_id)
            return {'message': 'User deleted.'}, 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message
    



    
