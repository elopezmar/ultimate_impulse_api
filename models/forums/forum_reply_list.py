from __future__ import annotations

from typing import TYPE_CHECKING

from firestore.collection import Collection
from models.forums.forum_reply import ForumReply

if TYPE_CHECKING:
    from models.forums.forum_topic import ForumTopic
    from models.users.user import User


class ForumReplyList():
    def __init__(self, topic: ForumTopic):
        self.topic = topic
        self.replies: list[ForumReply] = []

    @property
    def collection_path(self) -> str:
        return f'{self.topic.document_path}/replies'

    @property
    def collection(self) -> Collection:
        return Collection(self.collection_path)

    def from_dict(self, data: dict) -> ForumReplyList:
        self.replies = []
        for item in data.get('replies', []):
            reply = ForumReply(self.topic).from_dict(item)
            reply.retrieved = True
            self.replies.append(reply)
        return self

    def to_dict(self) -> dict:
        return {'replies': [reply.to_dict() for reply in self.replies]}

    def get(self, filters: list=None) -> ForumReplyList:
        data = self.collection.get(filters) 
        return self.from_dict({'replies': data})

    def delete(self, requestor: User) -> ForumReplyList:
        for reply in self.replies:
            reply.delete(requestor, update_topic_stats=False)
        return self
