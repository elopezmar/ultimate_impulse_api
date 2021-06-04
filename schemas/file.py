import base64
from marshmallow import Schema, fields

from gcp.storage import Storage


class FileSchema(Schema):
    url = fields.Str(required=True)
    b64_data = fields.Str(required=True, load_only=True)

    def read(self, file, dump=True):
        storage = Storage()
        file['url'] = storage.get_signed_url(file['url'])
        return self.dump(file) if dump else file

    def create(self, file, dump=True):
        storage = Storage()
        file_data = base64.b64decode(file['b64_data'])
        file['url'] = storage.upload(file_data)
        return self.dump(file) if dump else file

    @staticmethod
    def update(file):
        file_data = base64.b64decode(file['b64_data'])
        storage = Storage()
        storage.upload(file_data, file_url=file['url'])

    @staticmethod
    def delete(file):
        storage = Storage()
        storage.delete_file(file_url=file['url'])
