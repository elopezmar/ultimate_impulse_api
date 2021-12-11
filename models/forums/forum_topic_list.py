from __future__ import annotations
from copy import deepcopy

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
