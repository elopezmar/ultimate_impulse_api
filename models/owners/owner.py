from __future__ import annotations
from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound

from models.model import Model
from models.owners.owner_profile import OwnerProfile
from models.exceptions import BusinessError

if TYPE_CHECKING:
    from models.users.user import User


class Owner(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.username: str = None
        self.profile: OwnerProfile = OwnerProfile()

    @property
    def collection_path(self) -> str:
        return 'users'

    def from_user(self, user: User) -> Owner:
        return self.from_dict(user.to_dict())

    def get(self) -> Owner:
        try:
            return self.from_dict(self.document.get())
        except NotFound:
            raise BusinessError('User not found.', 404)
