from __future__ import annotations

from cloud_storage.file import File


class ReviewSection():
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.pic_url = None
        self.youtube_links: list[str] = []

    def from_dict(self, data: dict) -> ReviewSection:
        self.id = data.get('id')
        self.title = data.get('title')
        self.description = data.get('description')
        self.pic_url = data.get('pic_url')
        self.youtube_links = data.get('youtube_links', [])
        return self

    def to_dict(self) -> dict:
        data = {k: v for k, v in self.__dict__.items() if v}
        return data

    def set(self) -> ReviewSection:
        if self.pic_url:
            self.pic_url = File(
                prefix='reviews_section'
            ).overwrite(
                data=File(url=self.pic_url)
            ).accessibility(
                public=True
            ).url

        return self

    def update(self) -> ReviewSection:
        if self.pic_url:
            pic_file = File(url=self.pic_url)

            if pic_file.is_temp:
                self.pic_url = File(
                    prefix='reviews_section'
                ).overwrite(
                    data=pic_file
                ).accessibility(
                    public=True
                ).url

        return self

    def delete(self) -> ReviewSection:
        if self.pic_url:
            File(url=self.pic_url).delete()

        return self
    