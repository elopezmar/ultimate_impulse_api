from __future__ import annotations

import uuid

from cloud_storage.file import File
from firestore.document import Document
from models.irs.ir_file_list import IRFileList
from models.irs.ir_sample_list import IRSampleList
from models.irs.ir_review_list import IRReviewList
from models.irs.ir_stats import IRStats
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles


class IR():
    def __init__(self, id: str=None):
        self.id = id if id else uuid.uuid1().hex
        self.title = None
        self.description = None
        self.published_at = None
        self.owner = User()
        self.pics_urls: list[str] = []
        self.premium = None
        self.samples = IRSampleList(self)
        self.files = IRFileList(self)
        self.reviews = IRReviewList(self)
        self.stats = IRStats()
        self.tags: list[str] = []

    def get_path(self) -> str:
        return f'irs/{self.id}'

    def from_dict(self, data: dict) -> IR:
        self.id = data.get('id', self.id)
        self.title = data.get('title')
        self.description = data.get('description')
        self.published_at = data.get('published_at')
        self.owner.from_dict(data.get('owner', {}))
        self.pics_urls = data.get('pics_urls', [])
        self.premium = data.get('premium')
        self.samples.from_dict(data)
        self.files.from_dict(data)
        self.reviews.from_dict(data)
        self.stats.from_dict(data.get('stats', {}))
        self.tags = data.get('tags', [])

        return self

    def to_dict(self, collections: bool=True) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v}
        data.pop('samples', None)
        data.pop('files', None)
        data.pop('reviews', None)
        data['owner'] = self.owner.to_dict()
        data['stats'] = self.stats.to_dict()

        if collections:
            data.update(self.samples.to_dict())
            data.update(self.files.to_dict())
            data.update(self.reviews.to_dict())
        
        return data

    def get(self, requestor: User, samples: bool=False, files: bool=False, reviews: bool=False) -> IR:
        document = Document(self.get_path())
        self.from_dict(document.get())

        if samples:
            self.samples.get()
        if files:
            self.files.get(requestor)
        if reviews:
            self.reviews.get()

        return self

    def set(self, requestor: User) -> IR:
        if not requestor.role in [Roles.ADMIN, Roles.COLLABORATOR]:
            raise BusinessError("IR can't be created.", 400)

        self.owner = requestor
        self.stats.rating = 0
        self.stats.reviews = 0
        
        for idx, pic_url in enumerate(self.pics_urls):
            self.pics_urls[idx] = File(
                prefix='irs'
            ).overwrite(
                data=File(url=pic_url)
            ).accessibility(
                public=True
            ).url

        Document(self.get_path()).set(self.to_dict(collections=False))

        self.samples.set(requestor)
        self.files.set(requestor)

        return self.get(requestor, samples=True, files=True)

    def update(self, requestor: User) -> IR:
        current = IR(self.id).get(requestor)

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("IR can't be updated.", 400)

        if self.premium == None:
            self.premium = current.premium

        for idx, pic_url in enumerate(self.pics_urls):
            pic_file = File(url=pic_url)

            if pic_file.is_temp:
                self.pics_urls[idx] = File(
                    prefix='irs'
                ).overwrite(
                    data=pic_file
                ).accessibility(
                    public=True
                ).url

        if not self.pics_urls:
            self.pics_urls = current.pics_urls

        if not self.tags:
            self.tags = current.tags

        Document(self.get_path()).update(self.to_dict(collections=False))

        self.samples.update(requestor)
        self.files.update(requestor)

        return self.get(requestor, samples=True, files=True)

    def delete(self, requestor: User) -> IR:
        self.get(requestor)

        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("IR can't be deleted.", 400)

        self.samples.get().delete(requestor)
        self.files.get(requestor).delete(requestor)
        self.reviews.get().delete(requestor, update_ir_stats=False)

        for pic_url in self.pics_urls:
            File(url=pic_url).delete()

        Document(self.get_path()).delete()
        return self
