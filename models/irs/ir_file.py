from __future__ import annotations

from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound

from cloud_storage.file import File
from models.model import Model
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.irs.ir import IR
    from models.users.user import User


class IRFile(Model):
    def __init__(self, ir: IR, id: str=None):
        super().__init__(id)
        self.ir = ir
        self.title = None
        self.description = None
        self.file_url = None

    @property
    def collection_path(self) -> str:
        return f'{self.ir.document_path}/files'

    @property
    def remove_from_input(self) -> list:
        return ['ir']

    @property
    def remove_from_output(self) -> list:
        return ['ir']

    def calculate_url(self, requestor: User) -> IRFile:
        if self.ir.premium:
            if requestor.is_logged_in:
                self.file_url = File(url=self.file_url).signed_url
            else:
                self.file_url = None
        return self

    def get(self, requestor: User) -> IRFile:
        try:
            self.from_dict(self.document.get())
            self.calculate_url(requestor)
            self.retrieved = True
            return self
        except NotFound:
            raise BusinessError('File not found.', 404)
        
    def set(self, requestor: User) -> IRFile:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("File can't be created.", 400)

        self.file_url = File(
            prefix='irs_files'
        ).overwrite(
            data=File(url=self.file_url)
        ).accessibility(
            public=not self.ir.premium
        ).url

        data = self.document.set(self.to_dict())
        return self.from_dict(data)

    def update(self, requestor: User) -> IRFile:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("File can't be updated.", 400)

        if self.file_url:
            current = IRFile(self.ir, self.id).get(requestor)

            self.file_url = File(
                prefix='irs_files', url=current.file_url
            ).overwrite(
                data=File(url=self.file_url)
            ).accessibility(
                public=not self.ir.premium
            ).url

        data = self.document.update(self.to_dict())
        return self.from_dict(data)

    def delete(self, requestor: User) -> IRFile:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("File can't be deleted.", 400)

        if not self.retrieved:
            self.get(requestor)

        self.document.delete()
        File(url=self.file_url).delete()
        return self
