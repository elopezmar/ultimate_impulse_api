from __future__ import annotations

from models.model import Model


class ForumStats(Model):
    def __init__(self):
        super().__init__()
        self.topics: int = None
        self.replies: int = None

    @property
    def remove_from_output(self) -> list:
        return ['id']

    def set(self) -> ForumStats:
        self.topics = 0
        self.replies = 0
        return self
    
    def increment(self, topics: int=0, replies: int=0):
        self.topics += topics
        self.replies += replies
        return self
