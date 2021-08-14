from __future__ import annotations

from typing import TYPE_CHECKING

from firestore.collection import Collection
from models.irs.ir_review import IRReview

if TYPE_CHECKING:
    from models.irs.ir import IR
    from models.users.user import User

class IRReviewList():
    def __init__(self, ir: IR):
        self.ir = ir
        self.reviews: list[IRReview] = []

    def __get_path(self):
        return 'ir_user_reviews'

    def from_dict(self, data: dict) -> IRReviewList:
        self.reviews = []
        for item in data.get('reviews', []):
            self.reviews.append(IRReview(self.ir).from_dict(item))
        return self

    def to_dict(self) -> dict:
        return {'reviews': [review.to_dict() for review in self.reviews]}

    def get(self, filters: list=None) -> IRReviewList:
        if not filters:
            filters = []

        filters.append(('ir_id', '==', self.ir.id))

        collection = Collection(self.__get_path())
        data = collection.get(filters)
        
        self.reviews = []
        for item in data:
            self.reviews.append(IRReview(self.ir).from_dict(item))
        return self

    def set(self, requestor: User) -> IRReviewList:
        for review in self.reviews:
            review.set(requestor)
        return self

    def update(self, requestor: User) -> IRReviewList:
        for review in self.reviews:
            review.update(requestor)
        return self
    
    def delete(self, requestor: User, update_ir_stats: bool=True) -> IRReviewList:
        for review in self.reviews:
            review.delete(requestor, update_ir_stats)
        return self
        