from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound

from algolia.index import Index
from cloud_storage.file import File
from models.model import Model
from models.reviews.review_comment_list import ReviewCommentList
from models.reviews.review_content import ReviewContent
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.users.user import User
    

class Review(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.title: str = None
        self.description: str = None
        self.published_at: datetime = datetime.now()
        self.pic_url: str = None
        self.owner: Owner = Owner()
        self.content: ReviewContent = ReviewContent(self)
        self.comments: ReviewCommentList = ReviewCommentList(self)
        self.tags: list[str] = []

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
        try:
            self.from_dict(self.document.get())
            self.retrieved = True

            if content:
                self.content.get()
            if comments:
                self.comments.get()
        
            return self
        except NotFound:
            raise BusinessError('Review not found.', 404)
        
    def set(self, requestor: User) -> Review:
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
        self.document.set(self.to_dict(collections=False))
        self.content.set(requestor)
        self.get(content=True)

        self.index.save()
        return self


    def update(self, requestor: User) -> Review:
        current = Review(self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be updated.", 400)

        if self.pic_url:
            self.pic_url = File(
                prefix='reviews',
                url=current.pic_url
            ).overwrite(
                data=File(url=self.pic_url)
            ).accessibility(
                public=True
            ).url

        self.document.update(self.to_dict(collections=False))
        self.content.update(requestor)
        self.get(content=True)

        self.index.save()
        return self

    def delete(self, requestor: User) -> Review:
        if not self.retrieved:
            self.get()

        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be deleted.", 400)

        self.content.get().delete(requestor)
        self.comments.get().delete(requestor)

        if self.pic_url:
            File(url=self.pic_url).delete()

        self.document.delete()
        self.index.delete()
        return self
