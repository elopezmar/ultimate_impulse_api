from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from firestore.document import Document
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.irs.ir import IR


class IRReview():
    def __init__(self, ir: IR, id: str=None):
        self.ir = ir

        self.id = id if id else uuid.uuid1().hex
        self.ir_id = ir.id
        self.title = None
        self.description = None
        self.rating = None
        self.likes = None
        self.created_at = None
        self.owner = User()

    def __get_path(self) -> str:
        return f'ir_user_reviews/{self.id}'

    def from_dict(self, data: dict) -> IRReview:
        self.id = data.get('id', self.id)
        self.ir_id = data.get('ir_id', self.ir_id)
        self.title = data.get('title')
        self.description = data.get('description')
        self.rating = data.get('rating')
        self.likes = data.get('likes')
        self.created_at = data.get('created_at')
        self.owner.from_dict(data.get('owner', {}))

        return self

    def to_dict(self) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v}
        data.pop('ir', None)
        data['owner'] = self.owner.to_dict()
        return data

    def get(self) -> IRReview:
        document = Document(self.__get_path())
        return self.from_dict(document.get())

    def set(self, requestor: User) -> IRReview:
        if not requestor.is_logged_in:
            raise BusinessError("Review can't be created.", 400)

        self.owner = requestor
        document = Document(self.__get_path())
        data = document.set(self.to_dict())

        self.ir.get(requestor)
        self.ir.stats.rating = (
            (
                (self.ir.stats.reviews * self.ir.stats.rating) 
                + self.rating
            ) 
            / (self.ir.stats.reviews + 1)
        )
        self.ir.stats.reviews += 1
        self.ir.update(requestor=User(self.ir.owner.id))

        return self.from_dict(data)

    def update(self, requestor: User) -> IRReview:
        current = IRReview(self.ir, self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be updated.", 400)
        if current.ir_id != self.ir.id:
            raise BusinessError("Review doesn't belong to the IR.", 404)

        document = Document(self.__get_path())
        data = document.update(self.to_dict())

        if self.rating != None and current.rating != self.rating:
            self.ir.get(requestor)
            self.ir.stats.rating = (
                (
                    (self.ir.stats.reviews * self.ir.stats.rating) 
                    + (self.rating - current.rating)
                )
                / (self.ir.stats.reviews)
            )
            self.ir.update(requestor=User(self.ir.owner.id))

        return self.from_dict(data)

    def delete(self, requestor: User, update_ir_stats: bool=True) -> IRReview:
        self.get()

        if requestor.id not in [self.owner.id, self.ir.owner.id] and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be deleted.", 400)
        if self.ir_id != self.ir.id:
            raise BusinessError("Review doesn't belong to the IR.", 404)

        Document(self.__get_path()).delete()

        if update_ir_stats:
            self.ir.get(requestor)
            self.ir.stats.rating = (
                (
                    (self.ir.stats.reviews * self.ir.stats.rating) 
                    - self.rating
                ) 
                / (self.ir.stats.reviews - 1)
            )
            self.ir.stats.reviews -= 1
            self.ir.update(requestor=User(self.ir.owner.id))

        return self
