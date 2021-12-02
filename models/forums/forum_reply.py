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
        self.published_at: datetime = datetime.now()
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
            return BusinessError("Reply can't be created.", 400)

        self.owner.from_user(requestor)
        self.topic.update_stats(add_replies=1)
        return self._set()

    def update(self) -> ForumReply:
        current = ForumReply(self.topic, self.id).get()
        if requestor.id != current.owner.id and requestor.role != Roles.ADMIN:
            raise BusinessError("Reply can't be updated.", 400)
        return self._update()

    def delete(self, update_topic_stats: bool=True) -> ForumReply:
        self.get()
        owners = [self.owner.id, self.topic.owner.id]

        if requestor.id not in owners and requestor.role != Roles.ADMIN:
            raise BusinessError("Reply can't be deleted.", 400)

        if update_topic_stats:
            self.topic.update_stats(add_replies=-1)
            
        return self._delete()
