from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from firestore.document import Document
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.forums.forum_topic import ForumTopic


class ForumReply():
    def __init__(self, topic: ForumTopic, id: str=None):
        self.topic = topic
        self.retrieved = False

        self.id = id if id else uuid.uuid1().hex
        self.title = None
        self.description = None
        self.published_at = None
        self.owner = User()

    @property
    def document_path(self) -> str:
        return f'{self.topic.document_path}/replies/{self.id}'

    @property
    def document(self) -> Document:
        return Document(self.document_path)

    def from_dict(self, data: dict) -> ForumReply:
        self.id = data.get('id', self.id)
        self.title = data.get('title')
        self.description = data.get('description')
        self.published_at = data.get('published_at')
        self.owner.from_dict(data.get('owner', {}))
        return self

    def to_dict(self) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v}
        data.pop('topic', None)
        data.pop('retrieved', None)
        data['owner'] = self.owner.to_dict()
        return data

    def get(self) -> ForumReply:
        data = self.document.get()

        if data:
            self.from_dict(data)
            self.retrieved = True
            return self

        raise BusinessError('Reply not found', 400)

    def set(self, requestor: User) -> ForumReply:
        if not requestor.is_logged_in:
            return BusinessError("Reply can't be created.", 400)

        self.published_at = datetime.now()
        self.owner = requestor.owner_data()

        data = self.document.set(self.to_dict())
        self.topic.update_stats(add_replies=1)
        return self.from_dict(data)

    def update(self, requestor: User) -> ForumReply:
        current = ForumReply(self.topic, self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Reply can't be updated.", 400)

        data = self.document.update(self.to_dict())
        return self.from_dict(data)

    def delete(self, requestor: User, update_topic_stats: bool=True) -> ForumReply:
        if not self.retrieved:
            self.get()

        owners = [self.owner.id, self.topic.owner.id]

        if requestor.id not in owners and requestor.role != Roles.ADMIN:
            raise BusinessError("Reply can't be deleted.", 400)

        self.document.delete()

        if update_topic_stats:
            self.topic.update_stats(add_replies=-1)
            
        return self
