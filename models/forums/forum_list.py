from __future__ import annotations

from firestore.collection import Collection
from models.forums.forum import Forum


class ForumList():
    def __init__(self):
        self.forums: list[Forum] = []

    @property
    def collection_path(self) -> str:
        return f'forums'

    @property
    def collection(self) -> Collection:
        return Collection(self.collection_path)

    def from_dict(self, data: dict) -> ForumList:
        self.forums = []
        for item in data.get('forums', []):
            forum = Forum().from_dict(item)
            forum.retrieved = True
            self.forums.append(forum)
        return self

    def to_dict(self) -> dict:
        return {'forums': [topic.to_dict() for topic in self.forums]}

    def get(self, filters: list=None) -> ForumList:
        data = self.collection.get(filters) 
        return self.from_dict({'forums': data})
