from __future__ import annotations

from typing import TYPE_CHECKING

import flask_restful

from firestore.collection import Collection
from models.reviews.review import Review


class ReviewList():
    def __init__(self):
        self.reviews: list[Review] = []

    def __get_path(self):
        return 'reviews'

    def from_dict(self, data: dict) -> ReviewList:
        self.reviews = []
        for item in data.get('reviews', []):
            self.reviews.append(Review().from_dict(item))
        return self

    def to_dict(self) -> dict:
        return {'reviews': [review.to_dict() for review in self.reviews]}

    def get(self, filters: list=None):
        collection = Collection(self.__get_path())
        data = collection.get(filters)

        return self.from_dict({'reviews': data})
