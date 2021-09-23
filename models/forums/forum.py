from __future__ import annotations

import uuid
from datetime import datetime

from firestore.document import Document
from models.forums.forum_stats import ForumStats
from models.forums.forum_topic_list import ForumTopicList
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles


class Forum():
    def __init__(self, id: str=None):
        self.retrieved = False

        self.id = id if id else uuid.uuid1().hex
        self.title = None
        self.description = None
        self.published_at = None
        self.owner = User()
        self.stats = ForumStats()
        self.topics = ForumTopicList(self)

    @property
    def document_path(self) -> str:
        return f'forums/{self.id}'

    @property
    def document(self) -> Document:
        return Document(self.document_path)

    def from_dict(self, data: dict) -> Forum:
        self.id = data.get('id', self.id)
        self.title = data.get('title')
        self.description = data.get('description')
        self.published_at = data.get('published_at')
        self.owner.from_dict(data.get('owner', {}))
        self.stats.from_dict(data.get('stats', {}))
        self.topics.from_dict(data)
        return self

    def to_dict(self, collections: bool=True) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v}
        data.pop('retrieved', None)
        data.pop('topics', None)
        data['owner'] = self.owner.to_dict()
        data['stats'] = self.stats.to_dict()

        if collections:
            data.update(self.topics.to_dict())

        return data

    def update_stats(self, add_topics: int=0, add_replies: int=0) -> Forum:
        if not self.retrieved:
            self.get()

        self.stats.topics += add_topics
        self.stats.replies += add_replies
        data = self.document.update(self.to_dict(collections=False))
        return self.from_dict(data)

    def get(self, topics: bool=False) -> Forum:
        data = self.document.get()

        if data:
            self.from_dict(data)
            self.retrieved = True

            if topics:
                self.topics.get()

            return self
            
        raise BusinessError('Forum not found.', 404)
        

    def set(self, requestor: User) -> Forum:
        if requestor.role != Roles.ADMIN:
            return BusinessError("Forum can't be created.", 400)

        self.published_at = datetime.now()
        self.owner = requestor.owner_data()

        data = self.document.set(self.to_dict(collections=False))
        return self.from_dict(data)

    def update(self, requestor: User) -> Forum:
        if requestor.role != Roles.ADMIN:
            raise BusinessError("Forum can't be updated.", 400)

        data = self.document.update(self.to_dict(collections=False))
        return self.from_dict(data)

    def delete(self, requestor: User) -> Forum:
        if requestor.role != Roles.ADMIN:
            raise BusinessError("Forum can't be deleted.", 400)

        self.get(topics=True)
        self.topics.delete(requestor)
        self.document.delete()
        return self
