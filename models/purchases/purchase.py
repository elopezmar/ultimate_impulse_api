from __future__ import annotations

from datetime import datetime

from models.model import Model
from models.irs.ir import IR
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor


class Purchase(Model):
    def __init__(self, ir: IR=None, owner: Owner=None, id: str=None):
        super().__init__(id)
        self.ir: IR = ir or IR()
        self.owner: Owner = owner or Owner()
        self.purchased_at: datetime = None
        self.total: float = None

    @property
    def collection_path(self) -> str:
        return 'user_purchases'

    def get(self, ir_files: bool=False) -> Purchase:
        self._get()
        if ir_files:
            self.ir.files.get(force_signed_url=True)
        return self

    def set(self) -> Purchase:
        if not requestor.is_logged_in:
            raise BusinessError(400, 'Purchases only can be created by logged in users')
        
        self.ir.get()
        self.owner.from_user(requestor)
        self.purchased_at = datetime.now()
        self.total = self.ir.total
        self._set()
        self.ir.files.get(force_signed_url=True)
        return self

    def update(self) -> Purchase:
        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Purchases only can be updated by the owner or admin users')

        self.ir.get()
        self.owner.get()
        return self._update()

    def delete(self) -> Purchase:
        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Purchases only can be deleted by the owner or admin users')
        return self._delete()
