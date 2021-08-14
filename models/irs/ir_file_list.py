from __future__ import annotations

from typing import TYPE_CHECKING

from firestore.collection import Collection
from models.irs.ir_file import IRFile

if TYPE_CHECKING:
    from models.irs.ir import IR
    from models.users.user import User


class IRFileList():
    def __init__(self, ir: IR):
        self.ir = ir
        self.files: list[IRFile] = []

    def __get_path(self):
        return f'irs/{self.ir.id}/files'

    def from_dict(self, data: dict) -> IRFileList:
        self.files = []
        for item in data.get('files', []):
            self.files.append(IRFile(self.ir).from_dict(item))
        return self

    def to_dict(self) -> dict:
        return {'files': [file.to_dict() for file in self.files]}

    def get(self, requestor: User, filters: list=None) -> IRFileList:
        collection = Collection(self.__get_path())
        data = collection.get(filters)
        
        self.files = []
        for item in data:
            file = IRFile(self.ir).from_dict(item).calculate_url(requestor)
            self.files.append(file)
        return self

    def set(self, requestor: User) -> IRFileList:
        for file in self.files:
            file.set(requestor)
        return self

    def update(self, requestor: User) -> IRFileList:
        for file in self.files:
            file.update(requestor)
        return self
    
    def delete(self, requestor: User) -> IRFileList:
        for file in self.files:
            file.delete(requestor)
        return self
