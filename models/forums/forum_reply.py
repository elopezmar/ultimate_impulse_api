from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound

from models.model import Model
from models.users.user import User
from models.exceptions import BusinessError
from models.utils import Roles

if TYPE_CHECKING:
    from models.forums.forum_topic import ForumTopic


class ForumReply(Model):
    def __init__(self, topic: ForumTopic, id: str=None):
        super().__init__(id)
        self.topic = topic
        self.title = None
        self.description = None
        self.published_at = datetime.now()
        self.owner = User()

    @property
    def collection_path(self) -> str:
        return f'{self.topic.document_path}/replies'

    @property
    def remove_from_output(self) -> list:
        return ['topic']

    def get(self) -> ForumReply:
        try:
            self.from_dict(self.document.get())
            self.retrieved = True
            return self
        except NotFound:
            raise BusinessError('Reply not found.', 404)
        
    def set(self, requestor: User) -> ForumReply:
        if not requestor.is_logged_in:
            return BusinessError("Reply can't be created.", 400)

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
