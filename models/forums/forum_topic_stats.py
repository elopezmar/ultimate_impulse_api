from __future__ import annotations


class ForumTopicStats():
    def __init__(self):
        self.replies = 0

    def from_dict(self, data: dict) -> ForumTopicStats:
        self.replies = data.get('replies', 0)

    def to_dict(self) -> dict:
        data = {k: v for k, v in self.__dict__.items()}
        return data
