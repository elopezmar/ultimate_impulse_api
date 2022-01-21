from __future__ import annotations

from cloud_storage.file import File
from models.model import Model
from urllib.parse import urlparse


class ReviewSection(Model):
    def __init__(self):
        super().__init__()
        self.id = None
        self.title = None
        self.description = None
        self.pic_url = None
        self.youtube_links: list[str] = []

    def set(self) -> ReviewSection:
        if self.pic_url:
            self.pic_url = File(
                prefix='reviews_section'
            ).overwrite(
                data=File(url=self.pic_url)
            ).accessibility(
                public=True
            ).url

        links = self.youtube_links
        self.youtube_links = []

        for link in links:
            parsed = urlparse(link)
            if parsed.query != '':
                video_id = parsed.query.split('=')[1].split('&')[0]
                embed_link = f'https://www.youtube.com/embed/{video_id}'
                self.youtube_links.append(embed_link)

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
    