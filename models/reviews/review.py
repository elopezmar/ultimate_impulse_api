from __future__ import annotations
from datetime import datetime

from algolia.index import Index
from cloud_storage.file import File
from models.model import Model
from models.reviews.review_comment_list import ReviewCommentList
from models.reviews.review_content import ReviewContent
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor
    

class Review(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.title: str = None
        self.description: str = None
        self.published_at: datetime = None
        self.pic_url: str = None
        self.owner: Owner = Owner()
        self.content: ReviewContent = ReviewContent(self)
        self.comments: ReviewCommentList = ReviewCommentList(self)
        self.tags: list[str] = None

    @property
    def collection_path(self) -> str:
        return 'reviews'

    @property
    def index(self) -> Index:
        return Index(
            id=self.id,
            url=f'/review?id={self.id}&content=true&comments=true',
            title=self.title,
            type='review',
            description=self.description
        )

    def get(self, content: bool=False, comments: bool=False) -> Review:
        self._get()
        if content:
            self.content.get()
        if comments:
            self.comments.get()
        return self
        
    def set(self) -> Review:
        if not requestor.role in [Roles.ADMIN, Roles.COLLABORATOR]:
            raise BusinessError("Review can't be created.", 400)

        if self.pic_url:
            self.pic_url = File(
                prefix='reviews'
            ).overwrite(
                data=File(url=self.pic_url)
            ).accessibility(
                public=True
            ).url

        self.owner.from_user(requestor)
        self.published_at = datetime.now()
        self.tags = self.tags if self.tags else []
        self.index.save()
        self._set()
        self.content.set()
        return self.get(content=True)

    def update(self) -> Review:
        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be updated.", 400)

        current = Review(self.id).get()

        if self.pic_url:
            self.pic_url = File(
                prefix='reviews',
                url=current.pic_url
            ).overwrite(
                data=File(url=self.pic_url)
            ).accessibility(
                public=True
            ).url

        self.index.save()
        self._update()
        self.content.update()
        return self.get(content=True)

    def delete(self) -> Review:
        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be deleted.", 400)

        self.content.get().delete()
        self.comments.get().delete()
        self.index.delete()

        if self.pic_url:
            File(url=self.pic_url).delete()

        return self._delete()
