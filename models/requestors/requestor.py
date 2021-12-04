from __future__ import annotations
from datetime import datetime

from models.model import Model
from models.requestors.requestor_profile import RequestorProfile


class Requestor(Model):
    def __init__(self):
        super().__init__()
        self.email: str = None
        self.username: str = None
        self.created_at: datetime = None
        self.verified: bool = False
        self.role: str = None
        self.profile: RequestorProfile = RequestorProfile()

    @property
    def collection_path(self) -> str:
        return 'users'

    @property
    def entity_name(self) -> str:
        return 'User'
        
    @property
    def is_logged_in(self) -> bool:
        return self.role != None

    def reset(self) -> Requestor:
        self.__init__()
        return self

    def get(self, id: str) -> Requestor:
        self.reset()
        self.id = id
        return self._get()

