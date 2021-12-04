from __future__ import annotations

from typing import TYPE_CHECKING

from models.model_list import ModelList
from models.irs.ir_file import IRFile

if TYPE_CHECKING:
    from models.irs.ir import IR


class IRFileList(ModelList):
    def __init__(self, ir: IR):
        super().__init__()
        self.ir = ir
        self.items: list[IRFile] = []

    @property
    def item(self) -> IRFile:
        return IRFile(self.ir)

    def get(self, filters: list=None) -> IRFileList:
        self.retrieved = True
        self.from_list(self.collection.get(filters))
        for item in self.items:
            item.calculate_url()
        return self
