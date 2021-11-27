from __future__ import annotations
from typing import TYPE_CHECKING

from models.model import Model
from models.owners.owner_profile import OwnerProfile

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

    @property
    def entity_name(self) -> str:
        return 'User'

    def from_user(self, user: User) -> Owner:
        return self.from_dict(user.to_dict())
