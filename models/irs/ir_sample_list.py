from __future__ import annotations

from typing import TYPE_CHECKING

from firestore.collection import Collection
from models.irs.ir_sample import IRSample

if TYPE_CHECKING:
    from models.irs.ir import IR
    from models.users.user import User


class IRSampleList():
    def __init__(self, ir: IR):
        self.ir = ir
        self.samples: list[IRSample] = []

    def __get_path(self):
        return f'irs/{self.ir.id}/samples'

    def from_dict(self, data: dict) -> IRSampleList:
        self.samples = []
        for item in data.get('samples', []):
            self.samples.append(IRSample(self.ir).from_dict(item))
        return self

    def to_dict(self) -> dict:
        return {'samples': [sample.to_dict() for sample in self.samples]}

    def get(self, filters: list=None) -> IRSampleList:
        collection = Collection(self.__get_path())
        data = collection.get(filters)
        
        self.samples = []
        for item in data:
            self.samples.append(IRSample(self.ir).from_dict(item))
        return self

    def set(self, requestor: User) -> IRSampleList:
        for sample in self.samples:
            sample.set(requestor)
        return self

    def update(self, requestor: User) -> IRSampleList:
        for sample in self.samples:
            sample.update(requestor)
        return self
    
    def delete(self, requestor: User) -> IRSampleList:
        for sample in self.samples:
            sample.delete(requestor)
        return self
        