from __future__ import annotations


class ForumStats():
    def __init__(self):
        self.topics = 0
        self.replies = 0

    def from_dict(self, data: dict) -> ForumStats:
        self.topics = data.get('topics', 0)
        self.replies = data.get('replies', 0)

    def to_dict(self) -> dict:
        data = {k: v for k, v in self.__dict__.items()}
        return data
