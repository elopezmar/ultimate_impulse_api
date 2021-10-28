from __future__ import annotations
from datetime import datetime

from typing import Tuple

from google.api_core.exceptions import NotFound
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

from cloud_storage.file import File
from models.model import Model
from models.users.user_profile import UserProfile
from models.users.user_stats import UserStats
from models.users.user_list import UserList
from models.exceptions import BusinessError
from models.utils import Roles


class User(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.email = None
        self.password = None
        self.username = None
        self.created_at = datetime.now()
        self.verified = False
        self.role = None
        self.profile = UserProfile()
        self.stats = UserStats()
        self.old_password = None
        self.new_password = None

    @property
    def collection_path(self) -> str:
        return 'users'

    @property
    def remove_from_output(self) -> list:
        return ['old_password', 'new_password']

    @property
    def is_logged_in(self) -> bool:
        return self.role != None

    def get(self) -> User:
        try:
            self.from_dict(self.document.get())
            self.retrieved = True
            return self
        except NotFound:
            raise BusinessError('User not found.', 404)

    def set(self, requestor: User) -> User:
        if not self.role in [Roles.USER, Roles.ADMIN, Roles.COLLABORATOR]:
            raise BusinessError(f"Role {self.role} doesn't exists.", 400)
        if self.role in [Roles.ADMIN, Roles.COLLABORATOR] and not requestor.role == Roles.ADMIN:
            raise BusinessError('Only admin users can create admins or collaborators.', 400)
        if UserList().get([('email', '==', self.email)]).items:
            raise BusinessError('Email already exists.', 400)
        if UserList().get([('username', '==', self.username)]).items:
            raise BusinessError('Username already exists.', 400)
        if self.role in [Roles.ADMIN, Roles.COLLABORATOR]:
            self.verified = True

        data = self.document.set(self.to_dict())
        return self.from_dict(data)

    def update(self, requestor: User) -> User:
        if requestor.id == self.id:
            current = requestor
        elif requestor.role == Roles.ADMIN:
            current = User(self.id).get()
        else:
            raise BusinessError("User can't be updated.", 400)

        if self.username and self.username != current.username:
            if UserList().get([('username', '==', self.username)]).items:
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

        data = self.document.update(self.to_dict())
        return self.from_dict(data)

    def delete(self, requestor: User) -> User:
        if requestor.id != self.id and requestor.role != Roles.ADMIN:
            raise BusinessError("User can't be deleted.", 400)

        if not self.retrieved:
            self.get()

        self.document.delete()
        File(url=self.profile.pic_url).delete()
        return self

    def owner_data(self) -> User:
        owner = User(self.id)
        owner.email = None
        owner.password = None
        owner.username = self.username
        owner.created_at = None
        owner.verified = None
        owner.role = None
        owner.profile.pic_url = self.profile.pic_url
        owner.profile.country = self.profile.country
        owner.profile.social_media = self.profile.social_media
        owner.stats = None
        owner.old_password = None
        owner.new_password = None
        return owner

    def login(self) -> Tuple[str, User]:
        for user in UserList().get([('email', '==', self.email)]).items:
            if not user.verified:
                raise BusinessError('Invalid email or password.', 400)
            if not safe_str_cmp(user.password, self.password):
                raise BusinessError('User not verified.', 400)
            return create_access_token(user.id), user
        
        raise BusinessError('User not found.', 404)

    def verify(self):
        if not self.retrieved:
            self.get()

        self.verified = True
        self.document.update(self.to_dict())
