from __future__ import annotations

from models.model import Model


class UserStats(Model):
    def __init__(self):
        super().__init__()
        self.topics_created = 0

    @property
    def remove_from_output(self) -> list:
        return ['id']

    def set(self) -> UserStats:
        self.topics_created = 0
        return self
