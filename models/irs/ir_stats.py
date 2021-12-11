from __future__ import annotations

from models.model import Model


class IRStats(Model):
    def __init__(self):
        super().__init__()
        self.reviews = None
        self.rating = None
        
    @property
    def remove_from_output(self) -> list:
        return ['id']

    def set(self) -> IRStats:
        self.reviews = 0
        self.rating = 0
        return self

    def increment(self, reviews: int=0, rating: int=0) -> IRStats:
        self.rating = (
            ((self.reviews * self.rating) + rating) 
            / (self.reviews + reviews)
        )
        self.reviews += reviews
        return self