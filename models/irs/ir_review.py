from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound

from models.model import Model
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.irs.ir import IR


class IRReview(Model):
    def __init__(self, ir: IR, id: str=None):
        super().__init__(id)
        self.ir = ir
        self.ir_id = ir.id
        self.title = None
        self.description = None
        self.rating = 0
        self.likes = 0
        self.created_at = datetime.now()
        self.owner = User()

    @property
    def collection_path(self) -> str:
        return 'ir_user_reviews'

    @property
    def remove_from_input(self) -> list:
        return ['ir']

    @property
    def remove_from_output(self) -> list:
        return ['ir']

    def get(self) -> IRReview:
        try:
            self.from_dict(self.document.get())
            self.retrieved = True
            return self
        except NotFound:
            raise BusinessError('Review not found.')
        
    def set(self, requestor: User) -> IRReview:
        if not requestor.is_logged_in:
            raise BusinessError("Review can't be created.", 400)

        self.owner = requestor.owner_data()
        data = self.document.set(self.to_dict())
        self.ir.update_stats(add_reviews=1, rating=self.rating)

        return self.from_dict(data)

    def update(self, requestor: User) -> IRReview:
        current = IRReview(self.ir, self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be updated.", 400)
        if current.ir_id != self.ir.id:
            raise BusinessError("Review doesn't belong to the IR.", 404)

        data = self.document.update(self.to_dict())

        if self.rating != None and current.rating != self.rating:
            self.ir.update_stats(rating=(self.rating - current.rating))

        return self.from_dict(data)

    def delete(self, requestor: User, update_ir_stats: bool=True) -> IRReview:
        if not self.retrieved:
            self.get()

        if requestor.id not in [self.owner.id, self.ir.owner.id] and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be deleted.", 400)
        if self.ir_id != self.ir.id:
            raise BusinessError("Review doesn't belong to the IR.", 404)

        self.document.delete()

        if update_ir_stats:
            self.ir.update_stats(add_reviews=-1, rating=(self.rating * -1))

        return self
