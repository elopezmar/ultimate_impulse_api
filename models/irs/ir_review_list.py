from __future__ import annotations

from typing import TYPE_CHECKING

from models.model_list import ModelList
from models.irs.ir_review import IRReview

if TYPE_CHECKING:
    from models.irs.ir import IR
    from models.users.user import User


class IRReviewList(ModelList):
    def __init__(self, ir: IR):
        super().__init__()
        self.ir = ir
        self.items: list[IRReview] = []

    @property
    def item(self) -> IRReview:
        return IRReview(self.ir)

    def get(self, filters: list=None) -> IRReviewList:
        self.retrieved = True
        filters = filters if filters else []
        filters.append(('ir_id', '==', self.ir.id))
        return self.from_list(self.collection.get(filters))
    
    def delete(self, requestor: User, update_ir_stats: bool=True) -> IRReviewList:
        for review in self.items:
            review.delete(requestor, update_ir_stats)
        return self
        