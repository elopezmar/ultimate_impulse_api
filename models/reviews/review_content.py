from __future__ import annotations

from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound

from models.model_list import ModelList
from models.reviews.review_section import ReviewSection
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor

if TYPE_CHECKING:
    from models.reviews.review import Review


class ReviewContent(ModelList):
    def __init__(self, review: Review):
        self.name = 'content'
        self.review = review
        self.items: list[ReviewSection] = []

    @property
    def item(self) -> ReviewSection:
        return ReviewSection()

    @property
    def document_path(self) -> str:
        return f'{self.review.document_path}/content/{self.review.id}'

    def get(self) -> ReviewContent:
        try:
            self.from_dict(self.name, self.document.get())
            self.retrieved = True
            return self
        except NotFound:
            raise BusinessError(404, 'Review content not found')

    def set(self) -> ReviewContent:
        if requestor.id != self.review.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Review content only can be created by the review owner or admin users')

        for section in self.items:
            section.set()

        data = self.document.set(self.to_dict(self.name))
        return self.from_dict(self.name, data)

    def update(self) -> ReviewContent:
        if requestor.id != self.review.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Review content only can be updated by the review owner owner or admin users')

        for section in self.items:
            section.update()

        data = self.document.update(self.to_dict(self.name), overwrite=True)
        return self.from_dict(self.name, data)

    def delete(self) -> ReviewContent:
        if requestor.id != self.review.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Review content only can be deleted by the review owner owner or admin users')
            
        for section in self.items:
            section.delete()

        self.document.delete()
        return self
