from __future__ import annotations

from datetime import datetime

from google.api_core.exceptions import NotFound

from models.model import Model
from models.forums.forum_stats import ForumStats
from models.forums.forum_topic_list import ForumTopicList
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles


class Forum(Model):
    def __init__(self, id: str=None):
        super().__init__(id)
        self.title = None
        self.description = None
        self.published_at = datetime.now()
        self.owner = User()
        self.stats = ForumStats()
        self.topics = ForumTopicList(self)

    @property
    def collection_path(self) -> str:
        return 'forums'

    def update_stats(self, add_topics: int=0, add_replies: int=0) -> Forum:
        if not self.retrieved:
            self.get()

        self.stats.topics += add_topics
        self.stats.replies += add_replies
        data = self.document.update(self.to_dict(collections=False))
        return self.from_dict(data)

    def get(self, topics: bool=False) -> Forum:
        try:
            self.from_dict(self.document.get())
            self.retrieved = True

            if topics:
                self.topics.get()

            return self
        except NotFound:
            raise BusinessError('Forum not found.', 404)
            
    def set(self, requestor: User) -> Forum:
        if requestor.role != Roles.ADMIN:
            return BusinessError("Forum can't be created.", 400)

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

        if not self.retrieved:
            self.get()

        self.topics.get().delete(requestor)
        self.document.delete()
        return self
