from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp
from marshmallow import ValidationError

from resources.common.base import CollectionResource, DocumentResource

from schemas.user import UserSchema, UsersSchema
from schemas.common.exceptions import BusinessError
from schemas.common.security import Roles, Methods, Ownerships


class UserLogin(DocumentResource):
    def __init__(self, *args, **kwargs):
        super().__init__(UserSchema(), *args, **kwargs)
        self.security.set_privilege(Roles.ANONYMOUS, Methods.POST, Ownerships.ALL)

    def post(self):
        try:
            self.load_request_data()
            self.schema.partial = ('id', 'username',)

            login = self.schema.load(self.json)
            users = UsersSchema().get_documents(
                filters=[('email', '==', login['email'])], 
                to_list=True
            )
            if len(users) > 0:
                user = users[0]
                if user.get('verified'):
                    user_password = user['password'].encode('utf-8')
                    login_password = login['password'].encode('utf-8')
                    if safe_str_cmp(user_password, login_password):
                        access_token = create_access_token(identity=user['id'])
                        return {
                            'access_token': access_token,
                            'user': self.schema.dump(user)
                        }, 200
                    raise BusinessError('Invalid email or password.', 400)
                raise BusinessError('User not verified.', 400)
            raise BusinessError('User not found.', 404)
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message


class UserVerify(DocumentResource):
    def __init__(self, *args, **kwargs):
        super().__init__(UserSchema(), *args, **kwargs)
        self.security.set_privilege(Roles.ANONYMOUS, Methods.PUT, Ownerships.ALL)

    def put(self):
        try:
            self.load_request_data()

            self.schema.update_document(
                document={
                    'id': self.args['id'],
                    'verified': True
                }
            )
            return {'message': 'User verified.'}, 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message


class User(DocumentResource):
    def __init__(self, *args, **kwargs):
        super().__init__(UserSchema(), *args, **kwargs)
        self.security.set_privilege(Roles.ANONYMOUS, Methods.POST, Ownerships.ALL)

    @jwt_required(optional=True)
    def post(self):
        try:
            self.load_request_data()
            self.schema.partial = ('id',)

            user = self.schema.load(self.json)

            if Roles.exists(user['role']):
                if user['role'] in (Roles.ADMIN, Roles.COLLABORATOR):
                    if self.security.requestor['role'] == Roles.ADMIN:
                        user['verified'] = True
                    else:
                        raise BusinessError('Only admin users can create admins or collaborators.', 400)
                elif user['role'] == Roles.ANONYMOUS:
                    user['role'] = Roles.USER

            if len(UsersSchema().get_documents(
                filters=[('email', '==', user['email'])],
                to_list=True)) > 0:
                raise BusinessError('Email already exists.', 400)

            if len(UsersSchema().get_documents(
                filters=[('username', '==', user['username'])],
                to_list=True)) > 0:
                raise BusinessError('Username already exists.', 400)

            user = self.schema.set_document(user)
            return self.schema.dump(user), 201
        except ValidationError as err:
            return err.messages 
        except BusinessError as err:
            return err.message

    def get(self):
        try:
            self.load_request_data()
            user = {'id': self.args['id']}
            user = self.schema.get_document(user)
            return self.schema.dump(user), 200
        except KeyError:
            return {'message': 'An id must be provided as parameter.'}, 400
        except BusinessError as err:
            return err.message

    @jwt_required()
    def put(self):
        try:
            self.load_request_data()
            self.schema.only = ('id', 'old_password', 'new_password', 'username', 'profile')
            self.schema.partial = ('password', 'username', 'email')
            
            user = self.schema.load(self.json)

            new_user_name = user.get('username', None)
            old_password = user.pop('old_password', None)
            new_password = user.pop('new_password', None)
            temp_pic_url = user.get('profile', {}).get('pic_url', None)

            current_user = self.schema.get_document(user)
            current_username = current_user['username']
            current_password = current_user['password']
            current_pic_url = current_user.get('profile', {}).get('pic_url', None)

            if new_user_name and new_user_name != current_username:
                users = UsersSchema().get_documents(
                    filters=[('username', '==', new_user_name)], 
                    to_list=True
                )
                if len(users) > 0:
                    raise BusinessError('Username already exists.', 400)
                # TODO Update usernamme en todos los puntos

            if old_password and new_password:
                if not safe_str_cmp(old_password, current_password):
                    raise BusinessError('Old password is incorrect.', 400)
                elif safe_str_cmp(new_password, current_password):
                    raise BusinessError('New password cannot be old password.', 400)
                user['password'] = new_password

            if temp_pic_url:
                target_pic_url = self.storage.get_target_file_url(
                    temp_pic_url, current_pic_url
                )
                user['profile']['pic_url'] = target_pic_url

            self.schema.update_document(user)

            if temp_pic_url:
                self.storage.replace_file(
                    temp_pic_url, target_pic_url, make_public=True
                )

            return {'message': 'User updated.'}, 200
        except ValidationError as err:
            return err.messages 
        except BusinessError as err:
            return err.message

    @jwt_required()
    def delete(self):
        try:
            self.load_request_data()
            self.schema.only = ('id',)
            self.schema.partial = ('password', 'username', 'email')

            user = self.schema.load(self.json)
            user = self.schema.delete_document(user)

            pic_url = user.get('profile', {}).get('pic_url', None)

            if pic_url:
                self.storage.delete_file(pic_url, silent=True)
            
            return {'message': 'User deleted.'}, 200
        except ValidationError as err:
            return err.messages
        except BusinessError as err:
            return err.message
    

class Users(CollectionResource):
    def __init__(self, *args, **kwargs):
        super().__init__(UsersSchema(), *args, **kwargs)

    def get(self):
        try:
            self.load_request_data()
            users = self.schema.get_documents()
            return self.schema.dump(users), 200
        except BusinessError as err:
            return err.message
