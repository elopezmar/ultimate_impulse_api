from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from algolia.index import Index
from models.model import Model
from models.forums.forum_reply_list import ForumReplyList
from models.forums.forum_topic_stats import ForumTopicStats
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor

if TYPE_CHECKING:
    from models.forums.forum import Forum


class ForumTopic(Model):
    def __init__(self, forum: Forum, id: str=None):
        super().__init__(id)
        self.forum: Forum = forum
        self.title: str = None
        self.description: str = None
        self.published_at: datetime = None
        self.owner: Owner = Owner()
        self.stats: ForumTopicStats = ForumTopicStats()
        self.replies: ForumReplyList = ForumReplyList(self)

    @property
    def collection_path(self) -> str:
        return f'{self.forum.document_path}/topics'

    @property
    def entity_name(self) -> str:
        return 'Forum topic'

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

    def increment_stats(self, replies: int=0) -> ForumTopic:
        if not self.forum.disable_stats:
            self.get()
            self.stats.increment(replies)
            self.forum.increment_stats(replies=replies)
            return self._update()
        return self

    def get(self, replies: bool=False) -> ForumTopic:
        self._get()
        if replies:
            self.replies.get()
        return self

    def set(self) -> ForumTopic:
        if not requestor.is_logged_in:
            return BusinessError(400, 'Forum Topics only can be created by logged in users')

        self.owner.from_user(requestor)
        self.stats.set()
        self.published_at = datetime.now()
        self.forum.increment_stats(topics=1)
        self.index.save()
        return self._set()

    def update(self) -> ForumTopic:
        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Forum Topics only can be updated by the owner or admin users')

        self.index.save()
        return self._update()

    def delete(self) -> ForumTopic:
        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Forum Topics only can be deleted by the owner or admin users')

        self.forum.increment_stats(topics=-1)    
        self.replies.get().delete()
        self.index.delete()
        return self._delete()
