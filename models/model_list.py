from __future__ import annotations

import abc
from typing import List, TypeVar, TYPE_CHECKING

from firestore.collection import Collection
from firestore.document import Document

if TYPE_CHECKING:
    from models.model import Model
    from models.users.user import User

T = TypeVar('T', bound='ModelList')


class ModelList():
    def __init__(self):
        self.retrieved = False
        self.items: list[Model] = []

    @property
    @abc.abstractmethod
    def item(self) -> Model:
        pass

    @property
    def collection_path(self) -> str:
        return self.item.collection_path

    @property
    def collection(self) -> Collection:
        return Collection(self.collection_path)

    @property
    @abc.abstractmethod
    def document_path(self) -> str:
        pass

    @property
    def document(self) -> Document:
        return Document(self.document_path)

    def from_list(self: T, data: list[dict]) -> T:
        self.items = []
        for item in data:
            instance = self.item.from_dict(item)
            instance.retrieved = self.retrieved
            self.items.append(instance)
        return self

    def to_list(self) -> list[dict]:
        return [item.to_dict() for item in self.items]

    def from_dict(self: T, name: str, data: dict) -> T:
        return self.from_list(data.get(name, []))

    def to_dict(self, name: str) -> dict:
        return {name: self.to_list()}

    def get(self: T, filters: List[tuple]=None, order_by: List[tuple]=None, limit: int=None) -> T:
        self.retrieved = True
        return self.from_list(self.collection.get(filters, order_by, limit))

    def set(self: T, requestor: User) -> T:
        for item in self.items:
            item.set(requestor)
        return self

    def update(self: T, requestor: User) -> T:
        for item in self.items:
            item.update(requestor)
        return self
    
    def delete(self: T, requestor: User) -> T:
        for item in self.items:
            item.delete(requestor)
        return self
        