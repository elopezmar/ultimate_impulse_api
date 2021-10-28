from __future__ import annotations

from models.model import Model


class IRStats(Model):
    def __init__(self):
        super().__init__()
        self.reviews = 0
        self.rating = 0
        
    @property
    def remove_from_output(self) -> list:
        return ['id']
