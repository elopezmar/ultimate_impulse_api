from __future__ import annotations

from datetime import datetime

from google.api_core.exceptions import NotFound

from algolia.index import Index
from cloud_storage.file import File
from models.model import Model
from models.irs.ir_file_list import IRFileList
from models.irs.ir_sample_list import IRSampleList
from models.irs.ir_review_list import IRReviewList
from models.irs.ir_stats import IRStats
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles


class IR(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.title = None
        self.description = None
        self.published_at = datetime.now()
        self.owner = User()
        self.pics_urls: list[str] = []
        self.premium = False
        self.samples = IRSampleList(self)
        self.files = IRFileList(self)
        self.reviews = IRReviewList(self)
        self.stats = IRStats()
        self.tags: list[str] = []

    @property
    def collection_path(self) -> str:
        return 'irs'

    @property
    def index(self) -> Index:
        return Index(
            id=self.id,
            url=f'/ir?id={self.id}&samples=true&files=true&reviews=true',
            title=self.title,
            type='ir',
            description=self.description
        )

    def update_stats(self, add_reviews: int=0, rating: float=0):
        if not self.retrieved:
            self.get()

        self.stats.rating = (
            ((self.stats.reviews * self.stats.rating) + rating) 
            / (self.stats.reviews + add_reviews)
        )
        self.stats.reviews += add_reviews
        self.document.update(self.to_dict(collections=False))

    def get(self, requestor: User=None, samples: bool=False, files: bool=False, reviews: bool=False) -> IR:
        try:
            self.from_dict(self.document.get())
            self.retrieved = True

            if samples:
                self.samples.get()
            if files and requestor:
                self.files.get(requestor)
            if reviews:
                self.reviews.get()

            return self
        except NotFound:
            raise BusinessError('IR not found.', 404)
        
    def set(self, requestor: User) -> IR:
        if not requestor.role in [Roles.ADMIN, Roles.COLLABORATOR]:
            raise BusinessError("IR can't be created.", 400)

        self.owner = requestor.owner_data()
        
        for idx, pic_url in enumerate(self.pics_urls):
            self.pics_urls[idx] = File(
                prefix='irs'
            ).overwrite(
                data=File(url=pic_url)
            ).accessibility(
                public=True
            ).url

        self.document.set(self.to_dict(collections=False))
        self.samples.set(requestor)
        self.files.set(requestor)
        self.get(requestor, samples=True, files=True)

        self.index.save()
        return self

    def update(self, requestor: User) -> IR:
        current = IR(self.id).get()

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

        self.document.update(self.to_dict(collections=False))
        self.samples.update(requestor)
        self.files.update(requestor)
        self.get(requestor, samples=True, files=True)

        self.index.save()
        return self

    def delete(self, requestor: User) -> IR:
        if not self.retrieved:
            self.get()

        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("IR can't be deleted.", 400)

        self.samples.get().delete(requestor)
        self.files.get(requestor).delete(requestor)
        self.reviews.get().delete(requestor, update_ir_stats=False)

        for pic_url in self.pics_urls:
            File(url=pic_url).delete()

        self.document.delete()
        self.index.delete()
        return self
