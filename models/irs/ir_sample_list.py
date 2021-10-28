from __future__ import annotations

from typing import TYPE_CHECKING

from models.model_list import ModelList
from models.irs.ir_sample import IRSample

if TYPE_CHECKING:
    from models.irs.ir import IR


class IRSampleList(ModelList):
    def __init__(self, ir: IR):
        super().__init__()
        self.ir = ir
        self.items: list[IRSample] = []

    @property
    def item(self) -> IRSample:
        return IRSample(self.ir)
