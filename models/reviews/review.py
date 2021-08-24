from __future__ import annotations

import uuid

from cloud_storage.file import File
from firestore.document import Document
from models.reviews.review_comment_list import ReviewCommentList
from models.reviews.review_content import ReviewContent
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles
    

class Review():
    def __init__(self, id: str=None):
        self.id = id if id else uuid.uuid1().hex
        self.title = None
        self.description = None
        self.published_at = None
        self.pic_url = None
        self.owner = User()
        self.content = ReviewContent(self)
        self.comments = ReviewCommentList(self)
        self.tags: list[str] = []

    def __get_path(self) -> str:
        return f'reviews/{self.id}'

    def from_dict(self, data: dict) -> Review:
        self.id = data.get('id', self.id)
        self.title = data.get('title')
        self.description = data.get('description')
        self.published_at = data.get('published_at')
        self.pic_url = data.get('pic_url')
        self.owner.from_dict(data.get('owner', {}))
        self.content.from_dict(data)
        self.comments.from_dict(data)
        self.tags = data.get('tags', [])

        return self

    def to_dict(self, collections=True) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v}
        data.pop('content')
        data.pop('comments')
        data['owner'] = self.owner.to_dict()

        if collections:
            data.update(self.content.to_dict())
            data.update(self.comments.to_dict())

        return data

    def get(self, content: bool=False, comments: bool=False) -> Review:
        document = Document(self.__get_path())
        self.from_dict(document.get())

        if content:
            self.content.get()
        if comments:
            self.comments.get()
    
        return self

    def set(self, requestor: User) -> Review:
        if not requestor.role in [Roles.ADMIN, Roles.COLLABORATOR]:
            raise BusinessError("Review can't be created.", 400)

        self.owner = requestor.owner_data()

        if self.pic_url:
            self.pic_url = File(
                prefix='reviews'
            ).overwrite(
                data=File(url=self.pic_url)
            ).accessibility(
                public=True
            ).url

        Document(self.__get_path()).set(self.to_dict(collections=False))

        self.content.set(requestor)

        return self.get(content=True)


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

        self.published_at = current.published_at

        Document(self.__get_path()).update(self.to_dict(collections=False))

        self.content.update(requestor)

        return self.get(content=True)

    def delete(self, requestor: User) -> Review:
        self.get()

        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Review can't be deleted.", 400)

        self.content.get().delete(requestor)
        self.comments.get().delete(requestor)

        if self.pic_url:
            File(url=self.pic_url).delete()

        Document(self.__get_path()).delete()
        return self
