from __future__ import annotations

from models.model_list import ModelList
from models.reviews.review import Review


class ReviewList(ModelList):
    def __init__(self):
        self.items: list[Review] = []

    @property
    def item(self) -> Review:
        return Review()
