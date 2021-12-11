from __future__ import annotations

from cloud_storage.file import File
from models.model import Model


class UserProfile(Model):
    def __init__(self):
        super().__init__()
        self.first_name = None
        self.last_name = None
        self.born = None
        self.country = None
        self.pic_url = None
        self.social_media = None

    @property
    def remove_from_output(self) -> list:
        return ['id']

    def set(self) -> UserProfile:
        self.social_media = self.social_media if self.social_media else []
        return self

    def update(self, curren_pic_url: str=None) -> UserProfile:
        if self.pic_url:
            self.pic_url = File(
                prefix='users', url=curren_pic_url
            ).overwrite(
                data=File(url=self.pic_url)
            ).accessibility(
                public=True
            ).url
        return self

    def delete(self) -> UserProfile:
        File(url=self.pic_url).delete()
        return self
