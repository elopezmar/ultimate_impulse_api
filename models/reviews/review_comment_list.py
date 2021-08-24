from __future__ import annotations

from typing import TYPE_CHECKING

from firestore.collection import Collection
from models.reviews.review_comment import ReviewComment

if TYPE_CHECKING:
    from models.reviews.review import Review
    from models.users.user import User


class ReviewCommentList():
    def __init__(self, review: Review):
        self.review = review
        self.comments: list[ReviewComment] = []

    def __get_path(self):
        return 'review_user_comments'

    def from_dict(self, data: dict) -> ReviewCommentList:
        self.comments = []
        for item in data.get('comments', []):
            self.comments.append(ReviewComment(self.review).from_dict(item))
        return self

    def to_dict(self) -> dict:
        return {'comments': [comment.to_dict() for comment in self.comments]}

    def get(self, filters: list=None):
        if not filters:
            filters = []

        filters.append(('review_id', '==', self.review.id))

        collection = Collection(self.__get_path())
        data = collection.get(filters)

        return self.from_dict({'comments': data})

    def delete(self, requestor: User) -> ReviewCommentList:
        for comment in self.comments:
            comment.delete(requestor)
        return self