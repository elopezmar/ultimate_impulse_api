import uuid
from datetime import datetime
from flask_jwt_extended.utils import get_jwt_identity
from google.cloud.firestore_v1 import document
from marshmallow import Schema, fields, schema, validate
from google.api_core.exceptions import NotFound
from werkzeug.security import safe_str_cmp

from firestore import db, doc_to_dict, docs_to_dict, firestore
    
from schemas.exceptions import BusinessError
from schemas.utils import dict_to_dot_notation

class UserSchema(Schema):
    USERS = 'users'

    id = fields.Str(required=True, validate=validate.Length(equal=32))
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    username = fields.Str(required=True)
    created_at = fields.DateTime(missing=datetime.now())
    verified = fields.Boolean(missing=False)
    profile = fields.Nested(Schema.from_dict(dict(
        first_name = fields.Str(),
        last_name = fields.Str(),
        born = fields.Date(),
        country = fields.Str(),
        social_media = fields.List(fields.Url())
        # TODO Subir imagen de perfil        
    )))
    stats = fields.Nested(Schema.from_dict(dict(
        topics_created = fields.Number()
    )))

    @classmethod
    def get_collection_path(cls):
        return cls.USERS

    @classmethod
    def get_document_path(cls, user_id):
        return f'{cls.USERS}/{user_id}'

    def get_requestor_user(self):
        try:
            user_id = get_jwt_identity()
            return self.read(user_id, dump=False)
        except:
            raise BusinessError('JWT error.', 500)

    def create(self, user):
        user_id = uuid.uuid1().hex
        db.document(self.get_document_path(user_id)).set(user)
        user['id'] = user_id
        return self.dump(user)

    def read(self, user_id=None, user_email=None, user_username=None, raise_errors=True, dump=True):
        user = None
        if user_id:
            doc = db.document(self.get_document_path(user_id)).get()
            user = doc_to_dict(doc)                
        elif user_email:
            collection = self.get_collection_path()
            docs = db.collection(collection).where('email', '==', user_email).limit(1).stream()
            users = docs_to_dict(collection, docs)
            if len(users[collection]) > 0:
                user =  users[collection][0]
        elif user_username:
            collection = self.get_collection_path()
            docs = db.collection(collection).where('username', '==', user_username).limit(1).stream()
            users = docs_to_dict(collection, docs)
            if len(users[collection]) > 0:
                user =  users[collection][0]
        if user:
            return self.dump(user) if dump else user
        if raise_errors:
            raise BusinessError('User not found.', 404)
        
    def delete(self, user_id):
        requestor_user = self.get_requestor_user()
        if not requestor_user['id'] == user_id: # TODO Agregar la logica para los privilegios del usuario
            raise BusinessError('User cannot be deleted, insufficient privileges', 403)
        db.document(self.get_document_path(user_id)).delete()

        
class UserUpdateSchema(UserSchema):
    old_password = fields.Str()
    new_password = fields.Str()

    def update(self, user_id, user, validate_privileges=True):
        if validate_privileges:
            requestor_user = self.get_requestor_user()
            if not requestor_user['id'] == user_id: # TODO Agregar la logica para los privilegios del usuario
                raise BusinessError('User cannot be modified, insufficient privileges', 403)        
        if (
            user.get('username', None) or
            user.get('old_password', None) and user.get('new_password', None)
        ):
            original_user = self.read(user_id, dump=False)
            if user.get('username', None) and user['username'] != original_user['username']:
                if self.read(user_username=user['username'], raise_errors=False):
                    raise BusinessError('Username already exists.', 400)
                # TODO Update usernamme en todos los puntos
            if user.get('old_password', None) and user.get('new_password', None):
                if not safe_str_cmp(user['old_password'], original_user['password']):
                    raise BusinessError('Old password is incorrect.', 400)
                elif safe_str_cmp(user['new_password'], original_user['password']):
                    raise BusinessError('New password cannot be old password.', 400)
                user['password'] = user['new_password']
                user.pop('old_password', None)
                user.pop('new_password', None)
        try:
            user_ref = db.document(self.get_document_path(user_id))
            user_ref.update(dict_to_dot_notation(user))
        except NotFound:
            raise BusinessError('User not found.', 404)