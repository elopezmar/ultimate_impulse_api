from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from models.model import Model
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor

if TYPE_CHECKING:
    from models.irs.ir import IR


class IRReview(Model):
    def __init__(self, ir: IR, id: str=None):
        super().__init__(id)
        self.ir: IR = ir
        self.ir_id: str = ir.id
        self.title: str = None
        self.description: str = None
        self.rating: float = 0
        self.likes: int = 0
        self.created_at: datetime = datetime.now()
        self.owner: Owner = Owner()

    @property
    def collection_path(self) -> str:
        return 'ir_user_reviews'

    @property
    def entity_name(self) -> str:
        return 'IR review'

    @property
    def remove_from_input(self) -> list:
        return ['ir']

    @property
    def remove_from_output(self) -> list:
        return ['ir']

    def set(self) -> IRReview:
        if not requestor.is_logged_in:
            raise BusinessError("Review can't be created.", 400)

        self.owner.from_user(requestor)
        self.ir.update_stats(add_reviews=1, rating=self.rating)
        return self._set()

    def update(self) -> IRReview:
        current = IRReview(self.ir, self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be updated.", 400)
        if current.ir_id != self.ir.id:
            raise BusinessError("Review doesn't belong to the IR.", 404)

        if self.rating != None and current.rating != self.rating:
            self.ir.update_stats(rating=(self.rating - current.rating))

        return self._update()

    def delete(self, update_ir_stats: bool=True) -> IRReview:
        self.get()

        if requestor.id not in [self.owner.id, self.ir.owner.id] and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be deleted.", 400)
        if self.ir_id != self.ir.id:
            raise BusinessError("Review doesn't belong to the IR.", 404)

        if update_ir_stats:
            self.ir.update_stats(add_reviews=-1, rating=(self.rating * -1))

        return self._delete()
