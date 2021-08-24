from google.api_core.exceptions import NotFound
from google.cloud.firestore_v1.base_document import DocumentSnapshot

from firestore.client import client

from models.exceptions import BusinessError


class Document():
    def __init__(self, path: str):
        self.__client = client
        self.__ref = self.__client.document(path)

    @staticmethod
    def __to_dict(data: DocumentSnapshot) -> dict:
        if data.exists:
            return {'id': data.id, **data.to_dict()}
        return {}

    @classmethod
    def __to_dot_notation(cls, data: dict, prefix=None) -> dict:
        doted = {}
        for key, val in data.items():
            if isinstance(val, dict):
                p = f'{prefix}.{key}' if prefix else key
                doted.update(cls.__to_dot_notation(val, p))
            else:
                doted[f'{prefix}.{key}' if prefix else key] = val
        return doted

    def get(self) -> dict:
        return self.__to_dict(self.__ref.get())

    def set(self, data: dict) -> dict:
        data.pop('id', None)
        self.__ref.set(data)
        return self.get()

    def update(self, data: dict, overwrite=False) -> dict:
        try:
            if overwrite:
                return self.set(data)
            else:
                data.pop('id', None)
                data = self.__to_dot_notation(data)
                self.__ref.update(data)
                return self.get()
        except ValueError:
            raise BusinessError("Resource can't be updated because is empty.", 400)
        except NotFound:
            raise BusinessError("Resource not found.", 400)
        

    def delete(self):
        self.__ref.delete()
