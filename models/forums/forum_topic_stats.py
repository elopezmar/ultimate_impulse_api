from __future__ import annotations

from models.model import Model


class ForumTopicStats(Model):
    def __init__(self):
        super().__init__()
        self.replies: int = None

    @property
    def remove_from_output(self) -> list:
        return ['id']

    def set(self) -> ForumTopicStats:
        self.replies = 0
        return self

    def increment(self, replies: int) -> ForumTopicStats:
        self.replies += replies
        return self
