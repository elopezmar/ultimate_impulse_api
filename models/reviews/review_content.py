from __future__ import annotations

from typing import TYPE_CHECKING

from firestore.document import Document
from models.reviews.review_section import ReviewSection
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.reviews.review import Review
    from models.users.user import User


class ReviewContent():
    def __init__(self, review: Review):
        self.review = review
        self.content: list[ReviewSection] = []

    def __get_path(self) -> str:
        return f'reviews/{self.review.id}/content/{self.review.id}'

    def from_dict(self, data: dict) -> ReviewContent:
        self.content = []
        for item in data.get('content', []):
            self.content.append(ReviewSection().from_dict(item))
        return self

    def to_dict(self) -> dict:
        return {'content': [section.to_dict() for section in self.content]}

    def get(self) -> ReviewContent:
        document = Document(self.__get_path())
        return self.from_dict(document.get())

    def set(self, requestor: User) -> ReviewContent:
        if requestor.id != self.review.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Content can't be created.", 400)

        for section in self.content:
            section.set()

        document = Document(self.__get_path())
        data = document.set(self.to_dict())
        return self.from_dict(data)

    def update(self, requestor: User) -> ReviewContent:
        if requestor.id != self.review.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Content can't be updated.", 400)

        for section in self.content:
            section.update()

        document = Document(self.__get_path())
        data = document.update(self.to_dict(), overwrite=True)
        return self.from_dict(data)

    def delete(self, requestor: User) -> ReviewContent:
        if requestor.id != self.review.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Content can't be deleted.", 400)
            
        for section in self.content:
            section.delete()

        Document(self.__get_path()).delete()
        return self
