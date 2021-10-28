from __future__ import annotations

import models.users.user as models
from models.model_list import ModelList

class UserList(ModelList):
    def __init__(self):
        self.items: list[models.User] = []

    @property
    def item(self) -> models.User:
        return models.User()
