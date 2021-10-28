from __future__ import annotations

from models.model_list import ModelList
from models.forums.forum import Forum


class ForumList(ModelList):
    def __init__(self):
        super().__init__()
        self.items: list[Forum] = []

    @property
    def item(self) -> Forum:
        return Forum()
