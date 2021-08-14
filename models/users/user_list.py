from __future__ import annotations

import models.users.user as models
from firestore.collection import Collection


class UserList():
    def __init__(self):
        self.users: list[models.User] = []

    @staticmethod
    def __get_path():
        return 'users'

    @classmethod
    def from_dict(cls, data: dict) -> UserList:
        user_list = cls()
        for item in data.get('users', []):
            user_list.users.append(models.User().from_dict(item))
        return user_list

    def to_dict(self) -> dict:
        return {'users': [user.to_dict() for user in self.users]}

    @classmethod
    def get(cls, filters: list=None) -> UserList:
        collection = Collection(cls.__get_path())
        data = collection.get(filters)
        
        user_list = cls()
        for item in data:
            user_list.users.append(models.User().from_dict(item))
        return user_list
