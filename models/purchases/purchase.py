from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import datetime

from models.model import Model
from models.irs.ir import IR
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.users.user import User


class Purchase(Model):
    def __init__(self, ir: IR=None, owner: Owner=None, id: str=None):
        super().__init__(id)
        self.ir: IR = ir or IR()
        self.owner: Owner = owner or Owner()
        self.purchased_at: datetime = datetime.now()

    @property
    def collection_path(self) -> str:
        return 'user_purchases'

    def get(self) -> Purchase:
        return self.from_dict(self.document.get()) 

    def set(self, requestor: User) -> Purchase:
        if not requestor.is_logged_in:
            raise BusinessError("Purchase can't be created.", 400)
        
        self.ir.get()
        self.owner.from_user(requestor)
        data = self.document.set(self.to_dict())
        return self.from_dict(data)

    def update(self, requestor: User) -> Purchase:
        current = Purchase(id=self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Purchase can't be updated.", 400)

        self.ir = IR(id=current.ir.id).get()
        self.owner = Owner(id=current.owner.id).get()
        data = self.document.update(self.to_dict())
        return self.from_dict(data)

    def delete(self, requestor: User) -> Purchase:
        self.get()

        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Purchase can't be deleted.", 400)

        self.document.delete()
        return self
