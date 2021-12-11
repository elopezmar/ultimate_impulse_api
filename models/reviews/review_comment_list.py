from __future__ import annotations

from typing import TYPE_CHECKING

from models.model_list import ModelList
from models.reviews.review_comment import ReviewComment

if TYPE_CHECKING:
    from models.reviews.review import Review


class ReviewCommentList(ModelList):
    def __init__(self, review: Review):
        self.review = review
        self.items: list[ReviewComment] = []

    @property
    def item(self) -> ReviewComment:
        return ReviewComment(self.review)

    def get(self, filters: list=None):
        filters = filters if filters else []
        filters.append(('review_id', '==', self.review.id))
        return self.from_list(self.collection.get(filters))
