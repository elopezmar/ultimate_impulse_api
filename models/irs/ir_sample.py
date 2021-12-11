from __future__ import annotations

from typing import TYPE_CHECKING

from cloud_storage.file import File
from models.model import Model
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor

if TYPE_CHECKING:
    from models.irs.ir import IR


class IRSample(Model):
    def __init__(self, ir: IR, id: str=None):
        super().__init__(id)
        self.ir = ir
        self.title = None
        self.description = None
        self.file_url = None

    @property
    def collection_path(self) -> str:
        return f'{self.ir.document_path}/samples'

    @property
    def entity_name(self) -> str:
        return 'IR sample'

    @property
    def remove_from_input(self) -> list:
        return ['ir']

    @property
    def remove_from_output(self) -> list:
        return ['ir']

    def set(self) -> IRSample:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Sample can't be created.", 400)

        self.file_url = File(
            prefix='irs_samples'
        ).overwrite(
            data=File(url=self.file_url)
        ).accessibility(
            public=True
        ).url

        return self._set()

    def update(self) -> IRSample:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Sample can't be updated.", 400)

        current = IRSample(self.ir, self.id).get()

        self.file_url = File(
            prefix='irs_samples', url=current.file_url
        ).overwrite(
            data=File(url=self.file_url)
        ).accessibility(
            public=True
        ).url

        return self._update()

    def delete(self) -> IRSample:
        if requestor.id != self.ir.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Sample can't be deleted.", 400)

        File(url=self.file_url).delete()
        return self._delete()
