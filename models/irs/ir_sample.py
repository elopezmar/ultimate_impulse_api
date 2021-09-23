from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from cloud_storage.file import File
from firestore.document import Document
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.irs.ir import IR
    from models.users.user import User


class IRSample():
    def __init__(self, ir: IR, id: str=None):
        self.ir = ir

        self.id = id if id else uuid.uuid1().hex
        self.title = None
        self.description = None
        self.file_url = None

    def __get_path(self) -> str:
        return f'{self.ir.get_path()}/samples/{self.id}'

    def from_dict(self, data: dict) -> IRSample:
        self.id = data.get('id', self.id)
        self.title = data.get('title')
        self.description = data.get('description')
        self.file_url = data.get('file_url')

        return self

    def to_dict(self) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v}
        data.pop('ir', None)
        return data

    def get(self) -> IRSample:
        document = Document(self.__get_path())
        return self.from_dict(document.get())

    def set(self, requestor: User) -> IRSample:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Sample can't be created.", 400)

        self.file_url = File(
            prefix='irs_samples'
        ).overwrite(
            data=File(url=self.file_url)
        ).accessibility(
            public=True
        ).url

        document = Document(self.__get_path())
        data = document.set(self.to_dict())
        return self.from_dict(data)

    def update(self, requestor: User) -> IRSample:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Sample can't be updated.", 400)

        if self.file_url:
            current = IRSample(self.ir, self.id).get()

            self.file_url = File(
                prefix='irs_samples', url=current.file_url
            ).overwrite(
                data=File(url=self.file_url)
            ).accessibility(
                public=True
            ).url

        document = Document(self.__get_path())
        data = document.update(self.to_dict())
        return self.from_dict(data)

    def delete(self, requestor: User) -> IRSample:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Sample can't be deleted.", 400)

        self.get()
        Document(self.__get_path()).delete()
        File(url=self.file_url).delete()
        return self
