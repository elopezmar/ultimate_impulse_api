from __future__ import annotations

class UserProfile():
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.born = None
        self.country = None
        self.pic_url = None
        self.social_media = None

    def from_dict(self, data: dict) -> UserProfile:
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.born = data.get('born')
        self.country = data.get('country')
        self.pic_url = data.get('pic_url')
        self.social_media = data.get('social_media')
        return self

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v}

        