from __future__ import annotations
from datetime import datetime

from models.model import Model
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor


class Donation(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.owner: Owner = Owner()
        self.amount: float = None
        self.created_at: datetime = None

    @property
    def collection_path(self) -> str:
        return 'donations'

    def set(self) -> Donation:
        self.owner.from_user(requestor)
        self.created_at = datetime.now()
        return self._set()

    def delete(self) -> Donation:
        if requestor.role != Roles.ADMIN:
            raise BusinessError('Donations only can be deleted by admins.', 400)
        return self._delete()
