from __future__ import annotations
from datetime import datetime

from typing import Tuple

from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

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

    def set(self) -> User:
        self.role = self.role if self.role else Roles.USER
        self.verified = False

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

        self.created_at = datetime.now()
        self.profile.set()
        self.stats.set()
        return self._set()

    def update(self) -> User:
        if requestor.id != self.id and requestor.role != Roles.ADMIN:
            raise BusinessError("User can't be updated.", 400)

        current = User(self.id).get()

        if self.username and self.username != current.username:
            if UserList().get([('username', '==', self.username)]).items:
                raise BusinessError('Username already exists.', 400)
        
        if self.old_password and self.new_password:
            if not safe_str_cmp(self.old_password, current.password):
                raise BusinessError('Old password is incorrect.', 400)
            elif safe_str_cmp(self.new_password, current.password):
                raise BusinessError('New password cannot be old password.', 400)
            self.password = self.new_password

        self.profile.update(current.profile.pic_url)
        return self._update()

    def delete(self) -> User:
        if requestor.id != self.id and requestor.role != Roles.ADMIN:
            raise BusinessError("User can't be deleted.", 400)

        self.profile.delete()
        return self._delete()

    def login(self) -> Tuple[str, User]:
        for user in UserList().get([('email', '==', self.email)]).items:
            if not user.verified:
                raise BusinessError('User not verified.', 400)
            if not safe_str_cmp(user.password, self.password):
                raise BusinessError('Invalid email or password.', 400)
            return create_access_token(user.id), user
        raise BusinessError('User not found.', 404)

    def verify(self) -> User:
        self.verified = True
        return self._update()
