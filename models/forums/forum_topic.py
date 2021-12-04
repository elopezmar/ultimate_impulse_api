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
        self.published_at: datetime = datetime.now()
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

    def update_stats(self, add_replies: int=0) -> ForumTopic:
        self.get()
        self.stats.replies += add_replies
        self.forum.update_stats(add_replies=add_replies)
        return self._update()

    def get(self, replies: bool=False) -> ForumTopic:
        self._get()
        if replies:
            self.replies.get()
        return self

    def set(self) -> ForumTopic:
        if not requestor.is_logged_in:
            return BusinessError("Topic can't be created.", 400)

        self.owner.from_user(requestor)
        self.forum.update_stats(add_topics=1)
        self.index.save()
        return self._set()

    def update(self) -> ForumTopic:
        current = ForumTopic(self.forum, self.id).get()

        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Topic can't be updated.", 400)

        self.index.save()
        return self._update()

    def delete(self, update_forum_stats: bool=True) -> ForumTopic:
        self.get()

        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Topic can't be deleted.", 400)

        if update_forum_stats:
            self.forum.update_stats(add_topics=-1)
            
        self.replies.get().delete()
        self.index.delete()
        return self._delete()
