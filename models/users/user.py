from __future__ import annotations
from datetime import datetime

from typing import Tuple

from flask_restful import request
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

from mail.client import Client
from mail.messages.activate_account import activate_account

from models.model import Model
from models.users.user_profile import UserProfile
from models.users.user_stats import UserStats
from models.users.user_list import UserList
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor


class User(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.email: str = None
        self.password: str = None
        self.username: str = None
        self.created_at: datetime = None
        self.verified: bool = None
        self.role: str = None
        self.profile: UserProfile = UserProfile()
        self.stats: UserStats = UserStats()
        self.old_password: str = None
        self.new_password: str = None

    @property
    def collection_path(self) -> str:
        return 'users'

    @property
    def entity_name(self) -> str:
        return 'User'
        
    @property
    def remove_from_output(self) -> list:
        return ['old_password', 'new_password']

    def send_activation_email(self):
        link = f'{request.base_url}/verify?id={self.id}'
        mappings = {'username': self.username, 'link': link}
        Client().send_email(self.email, activate_account, mappings)

    def set(self) -> User:
        self.role = self.role if self.role else Roles.USER
        self.verified = False

        if not self.role in [Roles.USER, Roles.ADMIN, Roles.COLLABORATOR]:
            raise BusinessError(400, 'Invalid user role')
        if self.role in [Roles.ADMIN, Roles.COLLABORATOR] and not requestor.role == Roles.ADMIN:
            raise BusinessError(400, 'Only admin users can create collaborators or admin users')
        if UserList().get([('email', '==', self.email)]).items:
            raise BusinessError(400, 'Email already exists')
        if UserList().get([('username', '==', self.username)]).items:
            raise BusinessError(400, 'Username already exists')
        if self.role in [Roles.ADMIN, Roles.COLLABORATOR]:
            self.verified = True

        self.created_at = datetime.now()
        self.profile.set()
        self.stats.set()
        self._set()
        self.send_activation_email()
        return self

    def update(self) -> User:
        if requestor.id != self.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Users only can be updated by the owner or admin users')

        current = User(self.id).get()

        if self.username and self.username != current.username:
            if UserList().get([('username', '==', self.username)]).items:
                raise BusinessError(400, 'Username already exists')
        
        if self.old_password and self.new_password:
            if not safe_str_cmp(self.old_password, current.password):
                raise BusinessError(400, 'Old password is incorrect')
            elif safe_str_cmp(self.new_password, current.password):
                raise BusinessError(404, 'New password cannot be old password')
            self.password = self.new_password

        self.profile.update(current.profile.pic_url)
        return self._update()

    def delete(self) -> User:
        if requestor.id != self.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Users only can be deleted by the owner or admin users')

        self.profile.delete()
        return self._delete()

    def login(self) -> Tuple[str, User]:
        for user in UserList().get([('email', '==', self.email)]).items:
            if not user.verified:
                raise BusinessError(400, 'User not verified')
            if not safe_str_cmp(user.password, self.password):
                raise BusinessError(400, 'Invalid email or password')
            return create_access_token(user.id), user
        raise BusinessError(404, 'User not found')

    def verify(self) -> User:
        self.verified = True
        return self._update()
