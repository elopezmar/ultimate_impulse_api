from __future__ import annotations

from models.model import Model


class ForumStats(Model):
    def __init__(self):
        super().__init__()
        self.topics = 0
        self.replies = 0

    @property
    def remove_from_output(self) -> list:
        return ['id']
