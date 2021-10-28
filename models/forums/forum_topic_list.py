from __future__ import annotations

from typing import TYPE_CHECKING

from models.model_list import ModelList
from models.forums.forum_topic import ForumTopic

if TYPE_CHECKING:
    from models.users.user import User


class ForumTopicList(ModelList):
    def __init__(self, forum):
        super().__init__()
        self.forum = forum
        self.items: list[ForumTopic] = []

    @property
    def item(self) -> ForumTopic:
        return ForumTopic(self.forum)

    def delete(self, requestor: User) -> ForumTopicList:
        for topic in self.items:
            topic.delete(requestor, update_forum_stats=False)
        return self
