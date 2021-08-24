from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from firestore.document import Document
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.reviews.review import Review


class ReviewComment():
    def __init__(self, review: Review, id: str=None):
        self.review = review

        self.id = id if id else uuid.uuid1().hex
        self.review_id = review.id
        self.description = None
        self.created_at = None
        self.owner = User()

    def __get_path(self) -> str:
        return f'review_user_comments/{self.id}'

    def from_dict(self, data: dict) -> ReviewComment:
        self.id = data.get('id', self.id)
        self.review_id = data.get('review_id', self.review_id)
        self.description = data.get('description')
        self.created_at = data.get('created_at')
        self.owner.from_dict(data.get('owner', {}))
        return self

    def to_dict(self) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v}
        data.pop('review')
        data['owner'] = self.owner.to_dict()
        return data

    def get(self) -> ReviewComment:
        document = Document(self.__get_path())
        return self.from_dict(document.get())

    def set(self, requestor: User) -> ReviewComment:
        if not requestor.is_logged_in:
            raise BusinessError("Comment can't be created.", 400)

        self.owner = requestor.owner_data()
        document = Document(self.__get_path())
        data = document.set(self.to_dict())

        return self.from_dict(data)

    def update(self, requestor: User) -> ReviewComment:
        current = ReviewComment(self.review, self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Comment can't be updated.", 400)
        if current.review_id != self.review.id:
            raise BusinessError("Comment doesn't belong to the review.", 404)

        self.created_at = current.created_at
        document = Document(self.__get_path())
        data = document.update(self.to_dict())

        return self.from_dict(data)

    def delete(self, requestor: User) -> ReviewComment:
        self.get()

        if requestor.id not in [self.owner.id, self.review.owner.id] and requestor.role != Roles.ADMIN:
            raise BusinessError("Comment can't be deleted.", 400)
        if self.review_id != self.review.id:
            raise BusinessError("Comment doesn't belong to the review.", 404)

        Document(self.__get_path()).delete()
        return self
