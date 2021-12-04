from __future__ import annotations

from models.model import Model


class RequestorProfile(Model):
    def __init__(self):
        super().__init__()
        self.first_name = None
        self.last_name = None
        self.born = None
        self.country = None
        self.pic_url = None
        self.social_media = []

    @property
    def remove_from_output(self) -> list:
        return ['id']
