from __future__ import annotations

from models.model_list import ModelList
from models.forums.forum_topic import ForumTopic


class ForumTopicList(ModelList):
    def __init__(self, forum):
        super().__init__()
        self.forum = forum
        self.items: list[ForumTopic] = []

    @property
    def item(self) -> ForumTopic:
        return ForumTopic(self.forum)

    def delete(self) -> ForumTopicList:
        for topic in self.items:
            topic.delete(update_forum_stats=False)
        return self
