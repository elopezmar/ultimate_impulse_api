from __future__ import annotations
import uuid
from typing import Tuple

from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

from cloud_storage.file import File
from firestore.document import Document
from models.users.user_profile import UserProfile
from models.users.user_stats import UserStats
from models.users.user_list import UserList
from models.exceptions import BusinessError
from models.utils import Roles


class User():
    def __init__(self, id: str=None):
        self.id = id if id else uuid.uuid1().hex
        self.email = None
        self.password = None
        self.username = None
        self.created_at = None
        self.verified = None
        self.role = None
        self.profile = UserProfile()
        self.stats = UserStats()
        self.old_password = None
        self.new_password = None

    @property
    def is_logged_in(self) -> bool:
        return self.role != None

    def __get_path(self):
        return f'users/{self.id}'

    def from_dict(self, data: dict) -> User:
        self.id = data.get('id', self.id)
        self.email = data.get('email')
        self.password = data.get('password')
        self.username = data.get('username')
        self.created_at = data.get('created_at')
        self.verified = data.get('verified')
        self.role = data.get('role')
        self.profile.from_dict(data.get('profile', {}))
        self.stats.from_dict(data.get('stats', {}))
        self.old_password = data.get('old_password')
        self.new_password = data.get('new_password')
        return self

    def to_dict(self) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v}
        data['profile'] = self.profile.to_dict()
        data['stats'] = self.stats.to_dict()
        data.pop('old_password', None)
        data.pop('new_password', None)
        return data

    def get(self) -> User:
        document = Document(self.__get_path())
        return self.from_dict(document.get())

    def set(self, requestor: User) -> User:
        if not self.role in [Roles.USER, Roles.ADMIN, Roles.COLLABORATOR]:
            raise BusinessError(f"Role {self.role} doesn't exists.", 400)
        if self.role in [Roles.ADMIN, Roles.COLLABORATOR] and not requestor.role == Roles.ADMIN:
            raise BusinessError('Only admin users can create admins or collaborators.', 400)
        if UserList.get([('email', '==', self.email)]).users:
            raise BusinessError('Email already exists.', 400)
        if UserList.get([('username', '==', self.username)]).users:
            raise BusinessError('Username already exists.', 400)
        if self.role in [Roles.ADMIN, Roles.COLLABORATOR]:
            self.verified = True

        document = Document(self.__get_path())
        data = document.set(self.to_dict())
        return self.from_dict(data)

    def update(self, requestor: User) -> User:
        if requestor.id == self.id:
            current = requestor
        elif requestor.role == Roles.ADMIN:
            current = User(self.id).get()
        else:
            raise BusinessError("User can't be updated.", 400)

        if self.username and self.username != current.username:
            if UserList.get([('username', '==', self.username)]).users:
                raise BusinessError('Username already exists.', 400)
        
        if self.old_password and self.new_password:
            if not safe_str_cmp(self.old_password, current.password):
                raise BusinessError('Old password is incorrect.', 400)
            elif safe_str_cmp(self.new_password, current.password):
                raise BusinessError('New password cannot be old password.', 400)
            else:
                self.password = self.new_password

        if self.profile.pic_url:
            self.profile.pic_url = File(
                prefix='users', url=current.profile.pic_url
            ).overwrite(
                data=File(url=self.profile.pic_url)
            ).accessibility(
                public=True
            ).url

        document = Document(self.__get_path())
        data = document.update(self.to_dict())
        return self.from_dict(data)

    def delete(self, requestor: User) -> User:
        if requestor.id != self.id and requestor.role != Roles.ADMIN:
            raise BusinessError("User can't be deleted.", 400)

        self.get()
        Document(self.__get_path()).delete()
        File(url=self.profile.pic_url).delete()
        return self

    def owner_data(self) -> User:
        owner = User(self.id)
        owner.username = self.username
        owner.profile.country = self.profile.country
        owner.profile.social_media = self.profile.social_media
        return owner

    def login(self) -> Tuple[str, User]:
        for user in UserList.get([('email', '==', self.email)]).users:
            if not user.verified:
                raise BusinessError('Invalid email or password.', 400)
            if not safe_str_cmp(user.password, self.password):
                raise BusinessError('User not verified.', 400)
            return create_access_token(user.id), user
        
        raise BusinessError('User not found.', 404)

    def verify(self):
        self.verified = True
        document = Document(self.__get_path())
        document.update(self.to_dict())


