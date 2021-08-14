from __future__ import annotations

class UserStats():
    def __init__(self):
        self.topics_created = None

    def from_dict(self, data: dict) -> UserStats:
        self.topics_created = data.get('topics_created')
        return self

    def to_dict(self) -> dict:
        return {k: v for k, v in  self.__dict__.items() if v}