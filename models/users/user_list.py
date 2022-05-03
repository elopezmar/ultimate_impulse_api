from __future__ import annotations

import models.users.user as um
from models.model_list import ModelList

class UserList(ModelList):
    def __init__(self):
        self.items: list[um.User] = []

    @property
    def item(self) -> um.User:
        return um.User()

    def get_by_email(self, email: str) -> UserList:
        return self.get([('email', '==', email)])
