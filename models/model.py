from __future__ import annotations

import abc
import uuid
from typing import Any, Union, TypeVar, TYPE_CHECKING

from google.api_core.exceptions import NotFound

from algolia.index import Index
from firestore.document import Document
from models.model_list import ModelList
from models.exceptions import BusinessError

if TYPE_CHECKING:
    from models.users.user import User

T = TypeVar('T', bound='Model')


class Model():
    def __init__(self, id: str=None):
        self.id = id if id else uuid.uuid1().hex
        self.retrieved = False

    @property
    def __data(self) -> dict:
        return self.to_dict(collections=False)

    @__data.setter
    def __data(self, data: dict):
        self.from_dict(data)

    @property
    @abc.abstractmethod
    def collection_path(self) -> str:
        pass

    @property
    def document_path(self) -> str:
        return f'{self.collection_path}/{self.id}'

    @property
    def __document(self) -> Document:
        return Document(self.document_path)

    @property
    def entity_name(self) -> str:
        return self.__class__.__name__

    @property
    def remove_from_input(self) -> list:
        return []

    @property
    def remove_from_output(self) -> list:
        return []

    @property
    @abc.abstractmethod
    def index(self) -> Index:
        pass

    def from_dict(self: T, data: dict) -> T:
        remove = self.remove_from_input + ['retrieved']

        prop: str
        val: Union[Model, ModelList, Any]

        for prop, val in self.__dict__.items():
            if not prop in remove:
                is_model = issubclass(type(val), Model)
                is_modellist = issubclass(type(val), ModelList)

                if not is_model and not is_modellist:
                    setattr(self, prop, data.get(prop, val))
                elif is_modellist:
                    val.from_list(data.get(prop, []))
                elif is_model:
                    val.from_dict(data.get(prop, {}))

        return self
                    
    def to_dict(self, collections: bool=True) -> dict:
        data = {}
        remove = self.remove_from_output + ['retrieved']

        prop: str
        val: Union[Model, ModelList, Any]

        for prop, val in self.__dict__.items():
            if not prop in remove and val != None:
                is_model = issubclass(type(val), Model)
                is_modellist = issubclass(type(val), ModelList)

                if not is_model and not is_modellist:
                    data[prop] = val
                elif is_modellist and collections:
                    data[prop] = val.to_list()
                elif is_model:
                    data[prop] = val.to_dict()

        return data

    def _get(self: T) -> T:
        try:
            self.__data = self.__document.get()
            return self
        except NotFound:
            raise BusinessError(f'{self.entity_name} not found', 404)

    def _set(self: T) -> T:
        self.__data = self.__document.set(self.__data)
        return self

    def _update(self: T, overwrite: bool=False) -> T:
        self.__data = self.__document.update(self.__data, overwrite)
        return self

    def _delete(self: T) -> T:
        self.__data = self.__document.delete()
        return self

    def get(self: T) -> T:
        return self._get()

    @abc.abstractmethod
    def set(self: T, requestor: User) -> T:
        pass

    @abc.abstractmethod
    def update(self: T, requestor: User) -> T:
        pass
    
    @abc.abstractmethod
    def delete(self: T, requestor: User) -> T:
        pass
