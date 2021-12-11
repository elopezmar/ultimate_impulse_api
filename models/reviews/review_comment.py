from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from models.model import Model
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor

if TYPE_CHECKING:
    from models.reviews.review import Review


class ReviewComment(Model):
    def __init__(self, review: Review, id: str=None):
        super().__init__(id)
        self.review: Review = review
        self.review_id: str = review.id
        self.description: str = None
        self.created_at: datetime = None
        self.owner: Owner = Owner()

    @property
    def collection_path(self) -> str:
        return 'review_user_comments'

    @property
    def entity_name(self) -> str:
        return 'Review comment'

    @property
    def remove_from_output(self) -> list:
        return ['review']

    def set(self) -> ReviewComment:
        if not requestor.is_logged_in:
            raise BusinessError("Comment can't be created.", 400)

        self.owner.from_user(requestor)
        self.created_at = datetime.now()
        return self._set()

    def update(self) -> ReviewComment:
        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Comment can't be updated.", 400)
        if self.review_id != self.review.id:
            raise BusinessError("Comment doesn't belong to the review.", 404)

        return self._update()

    def delete(self) -> ReviewComment:
        owners = [self.owner.id, self.review.owner.id]
        
        if requestor.id not in owners and requestor.role != Roles.ADMIN:
            raise BusinessError("Comment can't be deleted.", 400)
        if self.review_id != self.review.id:
            raise BusinessError("Comment doesn't belong to the review.", 404)

        return self._delete()
