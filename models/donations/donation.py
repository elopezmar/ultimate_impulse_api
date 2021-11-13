from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound

from models.model import Model
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.users.user import User


class Donation(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.owner: Owner = Owner()
        self.amount: float = None
        self.created_at: datetime = datetime.now()

    @property
    def collection_path(self) -> str:
        return 'donations'

    def get(self) -> Donation:
        try:
            self.from_dict(self.document.get())
            self.retrieved = True
            return self
        except NotFound:
            raise BusinessError('Donation not found.', 404)

    def set(self, requestor: User) -> Donation:
        self.owner.from_user(requestor)
        data = self.document.set(self.to_dict())
        return self.from_dict(data)

    def delete(self, requestor: User) -> Donation:
        if requestor.role != Roles.ADMIN:
            raise BusinessError('Donations only can be deleted by admins.', 400)

        if not self.retrieved:
            self.get()

        self.document.delete()
        return self
