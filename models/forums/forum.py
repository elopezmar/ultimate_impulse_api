from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from models.model import Model
from models.forums.forum_stats import ForumStats
from models.forums.forum_topic_list import ForumTopicList
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.users.user import User


class Forum(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.title: str = None
        self.description: str = None
        self.published_at: datetime = datetime.now()
        self.owner: Owner = Owner()
        self.stats: ForumStats = ForumStats()
        self.topics: ForumTopicList = ForumTopicList(self)

    @property
    def collection_path(self) -> str:
        return 'forums'

    def update_stats(self, add_topics: int=0, add_replies: int=0) -> Forum:
        self.get()
        self.stats.topics += add_topics
        self.stats.replies += add_replies
        return self._update()

    def get(self, topics: bool=False) -> Forum:
        self._get()
        if topics:
            self.topics.get()
        return self
            
    def set(self, requestor: User) -> Forum:
        if requestor.role != Roles.ADMIN:
            return BusinessError("Forum can't be created.", 400)
        self.owner.from_user(requestor)
        return self._set()

    def update(self, requestor: User) -> Forum:
        if requestor.role != Roles.ADMIN:
            raise BusinessError("Forum can't be updated.", 400)
        return self._update()

    def delete(self, requestor: User) -> Forum:
        if requestor.role != Roles.ADMIN:
            raise BusinessError("Forum can't be deleted.", 400)
        self.topics.get().delete(requestor)
        return self._delete()
