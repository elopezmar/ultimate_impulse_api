from __future__ import annotations

from typing import TYPE_CHECKING

from cloud_storage.file import File
from models.model import Model
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor

if TYPE_CHECKING:
    from models.irs.ir import IR


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
    def entity_name(self) -> str:
        return 'IR File'

    @property
    def remove_from_input(self) -> list:
        return ['ir']

    @property
    def remove_from_output(self) -> list:
        return ['ir']

    def calculate_url(self) -> IRFile:
        if self.ir.premium:
            if requestor.is_logged_in:
                self.file_url = File(url=self.file_url).signed_url
            else:
                self.file_url = None
        return self

    def get(self) -> IRFile:
        self._get()
        self.calculate_url()
        return self
        
    def set(self) -> IRFile:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("File can't be created.", 400)

        self.file_url = File(
            prefix='irs_files'
        ).overwrite(
            data=File(url=self.file_url)
        ).accessibility(
            public=not self.ir.premium
        ).url

        return self._set()

    def update(self) -> IRFile:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("File can't be updated.", 400)

        if self.file_url:
            current = IRFile(self.ir, self.id).get()

            self.file_url = File(
                prefix='irs_files', url=current.file_url
            ).overwrite(
                data=File(url=self.file_url)
            ).accessibility(
                public=not self.ir.premium
            ).url

        return self._update()

    def delete(self) -> IRFile:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("File can't be deleted.", 400)

        self.get()
        File(url=self.file_url).delete()
        return self._delete()
