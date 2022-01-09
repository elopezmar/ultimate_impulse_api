from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from models.model import Model
from models.owners.owner import Owner
from models.exceptions import BusinessError
from models.utils import Roles
from resources.session import requestor

if TYPE_CHECKING:
    from models.forums.forum_topic import ForumTopic


class ForumReply(Model):
    def __init__(self, topic: ForumTopic, id: str=None):
        super().__init__(id)
        self.topic: ForumTopic = topic
        self.title: str = None
        self.description: str = None
        self.published_at: datetime = None
        self.owner: Owner = Owner()

    @property
    def collection_path(self) -> str:
        return f'{self.topic.document_path}/replies'

    @property
    def entity_name(self) -> str:
        return 'Forum reply'

    @property
    def remove_from_output(self) -> list:
        return ['topic']

    def set(self) -> ForumReply:
        if not requestor.is_logged_in:
            return BusinessError(400, 'Forum Replies only can be created by logged in users')

        self.owner.from_user(requestor)
        self.published_at = datetime.now()
        self.topic.increment_stats(replies=1)
        return self._set()

    def update(self) -> ForumReply:
        if requestor.id != self.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Forum Replies only can be updated by the owner or admin users')
        return self._update()

    def delete(self) -> ForumReply:
        owners = [self.owner.id, self.topic.owner.id]

        if requestor.id not in owners and requestor.role != Roles.ADMIN:
            raise BusinessError(400, 'Forum Replies only can be deleted by the owner or admin users')

        self.topic.increment_stats(replies=-1)
        return self._delete()
