from __future__ import annotations


class IRStats():
    def __init__(self):
        self.reviews = None
        self.rating = None

    def from_dict(self, data: dict) -> IRStats:
        self.reviews = data.get('reviews')
        self.rating = data.get('rating')

        return self

    def to_dict(self) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v != None}
        return data