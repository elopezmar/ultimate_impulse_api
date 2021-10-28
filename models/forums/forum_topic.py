from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound

from algolia.index import Index
from models.model import Model
from models.forums.forum_reply_list import ForumReplyList
from models.forums.forum_topic_stats import ForumTopicStats
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.forums.forum import Forum


class ForumTopic(Model):
    def __init__(self, forum: Forum, id: str=None):
        super().__init__(id)
        self.forum = forum
        self.title = None
        self.description = None
        self.published_at = datetime.now()
        self.owner = User()
        self.stats = ForumTopicStats()
        self.replies = ForumReplyList(self)

    @property
    def collection_path(self) -> str:
        return f'{self.forum.document_path}/topics'

    @property
    def remove_from_output(self) -> list:
        return ['forum']

    @property
    def index(self) -> Index:
        return Index(
            id=self.id,
            url=f'/forum/{self.forum.id}/topic?id={self.id}&replies=true',
            title=self.title,
            type='forum_topic',
            description=self.description
        )

    def update_stats(self, add_replies: int=0) -> ForumTopic:
        if not self.retrieved:
            self.get()

        self.stats.replies += add_replies
        data = self.document.update(self.to_dict(collections=False))
        self.forum.update_stats(add_replies=add_replies)
        return self.from_dict(data)

    def get(self, replies: bool=False) -> ForumTopic:
        try:
            self.from_dict(self.document.get())
            self.retrieved = True

            if replies:
                self.replies.get()

            return self
        except NotFound:
            raise BusinessError('Topic not found.', 404)

    def set(self, requestor: User) -> ForumTopic:
        if not requestor.is_logged_in:
            return BusinessError("Topic can't be created.", 400)

        self.owner = requestor.owner_data()
        data = self.document.set(self.to_dict(collections=False))
        self.forum.update_stats(add_topics=1)
        self.from_dict(data)

        self.index.save()
        return self

    def update(self, requestor: User) -> ForumTopic:
        current = ForumTopic(self.forum, self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Topic can't be updated.", 400)

        data = self.document.update(self.to_dict(collections=False))
        self.from_dict(data)

        self.index.save()
        return self

    def delete(self, requestor: User, update_forum_stats: bool=True) -> ForumTopic:
        if not self.retrieved:
            self.get()

        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Topic can't be deleted.", 400)

        self.replies.get().delete(requestor)
        self.document.delete()

        if update_forum_stats:
            self.forum.update_stats(add_topics=-1)
            
        self.index.delete()
        return self
