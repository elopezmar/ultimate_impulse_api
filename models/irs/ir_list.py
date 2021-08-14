from __future__ import annotations

from firestore.collection import Collection
from models.irs.ir import IR


class IRList():
    def __init__(self):
        self.irs: list[IR] = []

    def __get_path(self):
        return f'irs'

    def from_dict(self, data: dict) -> IRList:
        self.irs = []
        for item in data.get('irs', []):
            self.irs.append(IR().from_dict(item))
        return self

    def to_dict(self) -> dict:
        return {'irs': [ir.to_dict() for ir in self.irs]}

    def get(self, filters: list=[]) -> IRList:
        collection = Collection(self.__get_path())
        data = collection.get(filters)
        
        self.irs = []
        for item in data:
            self.irs.append(IR().from_dict(item))
        return self
