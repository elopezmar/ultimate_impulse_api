from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound

from models.model import Model
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.reviews.review import Review


class ReviewComment(Model):
    def __init__(self, review: Review, id: str=None):
        super().__init__(id)
        self.review = review
        self.review_id = review.id
        self.description = None
        self.created_at = datetime.now()
        self.owner = User()

    @property
    def collection_path(self) -> str:
        return 'review_user_comments'

    @property
    def remove_from_output(self) -> list:
        return ['review']

    def get(self) -> ReviewComment:
        try:
            self.from_dict(self.document.get())
            self.retrieved = True
            return self
        except NotFound:
            raise BusinessError('Comment not found.', 404)

    def set(self, requestor: User) -> ReviewComment:
        if not requestor.is_logged_in:
            raise BusinessError("Comment can't be created.", 400)

        self.owner = requestor.owner_data()
        data = self.document.set(self.to_dict())
        return self.from_dict(data)

    def update(self, requestor: User) -> ReviewComment:
        current = ReviewComment(self.review, self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Comment can't be updated.", 400)
        if current.review_id != self.review.id:
            raise BusinessError("Comment doesn't belong to the review.", 404)

        data = self.document.update(self.to_dict())
        return self.from_dict(data)

    def delete(self, requestor: User) -> ReviewComment:
        if not self.retrieved:
            self.get()

        if requestor.id not in [self.owner.id, self.review.owner.id] and requestor.role != Roles.ADMIN:
            raise BusinessError("Comment can't be deleted.", 400)
        if self.review_id != self.review.id:
            raise BusinessError("Comment doesn't belong to the review.", 404)

        self.document.delete()
        return self
