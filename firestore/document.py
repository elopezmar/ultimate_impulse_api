from google.api_core.exceptions import NotFound
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.document import DocumentReference

from firestore.cache import cache
from firestore.client import client


class Document():
    def __init__(self, path: str):
        self.path: str = path
        self.data: dict = {}

    @property
    def ref(self) -> DocumentReference:
        return client.document(self.path)

    @staticmethod
    def to_dict(data: DocumentSnapshot) -> dict:
        if data.exists:
            return {'id': data.id, **data.to_dict()}
        raise NotFound('Document not found.')

    @classmethod
    def to_dot_notation(cls, data: dict, prefix=None) -> dict:
        doted = {}
        for key, val in data.items():
            if isinstance(val, dict):
                p = f'{prefix}.{key}' if prefix else key
                doted.update(cls.to_dot_notation(val, p))
            else:
                doted[f'{prefix}.{key}' if prefix else key] = val
        return doted

    def get(self) -> dict:
        self.data = cache.get(self.path)
        if not self.data:
            self.data = cache.set(self.path, self.to_dict(self.ref.get()))
        return self.data

    def set(self, data: dict) -> dict:
        self.data = cache.set(self.path, data)
        data.pop('id', None)
        self.ref.set(data)
        return self.data

    def update(self, data: dict, overwrite=False) -> dict:
        if overwrite:
            return self.set(data)
        else:
            self.get()
            self.data = cache.update(self.path, data)
            data.pop('id', None)
            data = self.to_dot_notation(data)
            self.ref.update(data)
            return self.data
                
    def delete(self) -> dict:
        self.get()
        self.ref.delete()
        cache.delete(self.path)
        return self.data
