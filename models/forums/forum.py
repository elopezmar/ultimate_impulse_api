from __future__ import annotations
from datetime import datetime

from models.model import Model
from models.forums.forum_stats import ForumStats
from models.forums.forum_topic_list import ForumTopicList
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor


class Forum(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.title: str = None
        self.description: str = None
        self.published_at: datetime = None
        self.owner: Owner = Owner()
        self.stats: ForumStats = ForumStats()
        self.topics: ForumTopicList = ForumTopicList(self)
        self.disable_stats: bool = False

    @property
    def collection_path(self) -> str:
        return 'forums'

    @property
    def remove_from_output(self) -> list:
        return ['disable_stats']

    def increment_stats(self, topics: int=0, replies: int=0) -> Forum:
        if not self.disable_stats:
            self.get()
            self.stats.increment(topics, replies)
            return self._update()
        return self

    def get(self, topics: bool=False) -> Forum:
        self._get()
        if topics:
            self.topics.get()
        return self
            
    def set(self) -> Forum:
        if requestor.role != Roles.ADMIN:
            return BusinessError(400, 'Forums only can be created by admin users')
        self.owner.from_user(requestor)
        self.stats.set()
        self.published_at = datetime.now()
        return self._set()

    def update(self) -> Forum:
        if requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Forums only can be updated by admin users')
        return self._update()

    def delete(self) -> Forum:
        if requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Forums only can be deleted by admin users')
        self.disable_stats = True
        self.topics.get().delete()
        return self._delete()
