from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from firestore.document import Document
from models.forums.forum_reply_list import ForumReplyList
from models.forums.forum_topic_stats import ForumTopicStats
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.forums.forum import Forum


class ForumTopic():
    def __init__(self, forum: Forum, id: str=None):
        self.forum = forum
        self.retrieved = False

        self.id = id if id else uuid.uuid1().hex
        self.title = None
        self.description = None
        self.published_at = None
        self.owner = User()
        self.stats = ForumTopicStats()
        self.replies = ForumReplyList(self)

    @property
    def document_path(self) -> str:
        return f'{self.forum.document_path}/topics/{self.id}'

    @property
    def document(self) -> Document:
        return Document(self.document_path)

    def from_dict(self, data: dict) -> ForumTopic:
        self.id = data.get('id', self.id)
        self.title = data.get('title')
        self.description = data.get('description')
        self.published_at = data.get('published_at')
        self.owner.from_dict(data.get('owner', {}))
        self.stats.from_dict(data.get('stats', {}))
        self.replies.from_dict(data)
        return self

    def to_dict(self, collections: bool=True) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v}
        data.pop('forum', None)
        data.pop('retrieved', None)
        data.pop('replies', None)
        data['owner'] = self.owner.to_dict()
        data['stats'] = self.stats.to_dict()

        if collections:
            data.update(self.replies.to_dict())

        return data

    def update_stats(self, add_replies: int=0) -> ForumTopic:
        if not self.retrieved:
            self.get()

        self.stats.replies += add_replies
        data = self.document.update(self.to_dict(collections=False))
        self.forum.update_stats(add_replies=add_replies)
        return self.from_dict(data)

    def get(self, replies: bool=False) -> ForumTopic:
        data = self.document.get()

        if data:
            self.from_dict(data)
            self.retrieved = True

            if replies:
                self.replies.get()

            return self

        raise BusinessError('Topic not found.', 404)

    def set(self, requestor: User) -> ForumTopic:
        # TODO: Quien podre crear topicos
        if not requestor.is_logged_in:
            return BusinessError("Topic can't be created.", 400)

        self.published_at = datetime.now()
        self.owner = requestor.owner_data()

        data = self.document.set(self.to_dict(collections=False))
        self.forum.update_stats(add_topics=1)
        return self.from_dict(data)

    def update(self, requestor: User) -> ForumTopic:
        current = ForumTopic(self.forum, self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Topic can't be updated.", 400)

        data = self.document.update(self.to_dict(collections=False))
        return self.from_dict(data)

    def delete(self, requestor: User, update_forum_stats: bool=True) -> ForumTopic:
        if not self.retrieved:
            self.get()

        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Topic can't be deleted.", 400)

        self.replies.get().delete(requestor)
        self.document.delete()

        if update_forum_stats:
            self.forum.update_stats(add_topics=-1)
            
        return self
