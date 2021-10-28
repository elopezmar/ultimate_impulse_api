from __future__ import annotations

from models.model_list import ModelList
from models.irs.ir import IR


class IRList(ModelList):
    def __init__(self):
        super().__init__()
        self.items: list[IR] = []

    @property
    def item(self) -> IR:
        return IR()
