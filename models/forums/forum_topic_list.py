from __future__ import annotations

from typing import TYPE_CHECKING

from firestore.collection import Collection
from models.forums.forum_topic import ForumTopic

if TYPE_CHECKING:
    from models.users.user import User


class ForumTopicList():
    def __init__(self, forum):
        self.forum = forum
        self.topics: list[ForumTopic] = []

    @property
    def collection_path(self) -> str:
        return f'{self.forum.document_path}/topics'

    @property
    def collection(self) -> Collection:
        return Collection(self.collection_path)

    def from_dict(self, data: dict) -> ForumTopicList:
        self.topics = []
        for item in data.get('topics', []):
            topic = ForumTopic(self.forum).from_dict(item)
            topic.retrieved = True
            self.topics.append(topic)
        return self

    def to_dict(self) -> dict:
        return {'topics': [topic.to_dict() for topic in self.topics]}

    def get(self, filters: list=None) -> ForumTopicList:
        data = self.collection.get(filters) 
        return self.from_dict({'topics': data})

    def delete(self, requestor: User) -> ForumTopicList:
        for topic in self.topics:
            topic.delete(requestor, update_forum_stats=False)
        return self
