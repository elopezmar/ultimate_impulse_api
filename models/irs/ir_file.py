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
    def remove_from_output(self) -> list:
        return ['ir']

    def calculate_url(self, force_signed_url: bool=False) -> IRFile:
        if force_signed_url or (requestor.is_logged_in and not self.ir.premium):
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
            raise BusinessError(400, 'IR Files only can be created by the IR owner or admin users')

        self.file_url = File(
            prefix='irs_files'
        ).overwrite(
            data=File(url=self.file_url)
        ).accessibility(
            public=False
        ).url

        return self._set()

    def update(self) -> IRFile:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'IR Files only can be updated by the IR owner or admin users')

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
            raise BusinessError(400, 'IR Files only can be deleted by the IR owner or admin users')

        File(url=self.file_url).delete()
        return self._delete()
