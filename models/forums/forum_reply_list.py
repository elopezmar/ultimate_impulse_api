from __future__ import annotations

from typing import TYPE_CHECKING

from models.model_list import ModelList
from models.forums.forum_reply import ForumReply

if TYPE_CHECKING:
    from models.forums.forum_topic import ForumTopic
    from models.users.user import User


class ForumReplyList(ModelList):
    def __init__(self, topic: ForumTopic):
        self.topic = topic
        self.items: list[ForumReply] = []

    @property
    def item(self) -> ForumReply:
        return ForumReply(self.topic)

    def delete(self, requestor: User) -> ForumReplyList:
        for reply in self.items:
            reply.delete(requestor, update_topic_stats=False)
        return self
