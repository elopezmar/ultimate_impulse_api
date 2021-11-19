from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound

from algolia.index import Index
from cloud_storage.file import File
from models.model import Model
from models.irs.ir_file_list import IRFileList
from models.irs.ir_sample_list import IRSampleList
from models.irs.ir_review_list import IRReviewList
from models.irs.ir_stats import IRStats
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.users.user import User


class IR(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.title: str = None
        self.description: str = None
        self.published_at: datetime = None
        self.owner: Owner = Owner()
        self.pics_urls: list[str] = []
        self.premium: bool = None
        self.price: float = None
        self.discount: float = None
        self.total: float = None
        self.samples: IRSampleList = IRSampleList(self)
        self.files: IRFileList = IRFileList(self)
        self.reviews: IRReviewList = IRReviewList(self)
        self.stats: IRStats = IRStats()
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

    def calculate_price(self):
        self.price = self.price if self.price != None else 0
        self.discount = self.discount if self.discount != None else 0
        self.total = self.price - (self.price * (self.discount/100))

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

        self.owner.from_user(requestor)
        self.published_at = datetime.now()

        if self.premium == None:
            self.premium = False
        
        for idx, pic_url in enumerate(self.pics_urls):
            self.pics_urls[idx] = File(
                prefix='irs'
            ).overwrite(
                data=File(url=pic_url)
            ).accessibility(
                public=True
            ).url

        self.calculate_price()
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

        if self.premium == None:
            self.premium = current.premium

        if self.price == None:
            self.price = current.price

        if self.discount == None:
            self.discount = current.discount

        if self.total == None:
            self.total = current.total

        if self.pics_urls == None:
            self.pics_urls = current.pics_urls

        if self.tags == None:
            self.tags = current.tags

        self.calculate_price()
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
