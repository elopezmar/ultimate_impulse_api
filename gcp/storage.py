import datetime

from schemas.common.exceptions import BusinessError
from uuid import uuid1
from google.cloud import storage

class Storage():
    storage_client = None
    bucket = None

    def __init__(self, schema_name='temp'):
        self.schema_name = schema_name
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket('storage-ui-dev') # TODO Agregar a variable de entorno
    
    def upload(self, file_data: bytes, file_url=None, schema_name=None):
        if file_url:
            file_name = self.get_file_name(file_url)
        else:
            file_name = self.get_new_file_name(schema_name)
        blob = self.bucket.blob(file_name)
        blob.upload_from_string(file_data)
        return blob.public_url

    def delete_file(self, file_url, silent=False):
        file_name = self.get_file_name(file_url)
        blob = self.bucket.blob(file_name)

        if blob.exists():
            blob.delete()
        elif not silent:
            raise BusinessError(f"File {file_url} not found.", 404)

    def replace_file(self, temp_file_url, target_file_url, make_public=False):
        temp_file_name = self.get_file_name(temp_file_url)
        target_file_name = self.get_file_name(target_file_url)

        if temp_file_url == target_file_url:
            target_blob = self.bucket.blob(target_file_name)
        else:
            self.delete_file(target_file_url, silent=True)
            temp_blob = self.bucket.blob(temp_file_name)
            target_blob = self.bucket.rename_blob(temp_blob, target_file_name)

        if make_public:
            target_blob.make_public()

        return target_blob.public_url
        
    def get_signed_url(self, file_url):
        file_name = self.get_file_name(file_url)
        blob = self.bucket.blob(file_name)
        signed_url = blob.generate_signed_url(
            version='v4',
            # TODO: Definir el tiempo de expiración para los archivos privados
            expiration=datetime.timedelta(minutes=15),
            method='GET'
        )
        return signed_url

    def get_target_file_url(self, temp_file_url, current_file_url=None):
        if temp_file_url == current_file_url:
            return current_file_url

        temp_file_name = self.get_file_name(temp_file_url)
        temp_blob = self.bucket.blob(temp_file_name)

        if not temp_blob.exists():
            raise BusinessError(f"File {temp_file_url} not found.", 404)

        if not current_file_url:
            file_id = self.get_file_id(temp_file_url)
            storage_url = self.get_storage_url(temp_file_url)
            file_name = self.get_new_file_name(file_id)
            return storage_url + file_name
        return current_file_url

    def get_new_file_name(self, file_id=None):
        if not file_id:
            file_id = uuid1().hex
        return f'{self.schema_name.lower()}_{file_id}'

    @staticmethod
    def get_file_name(file_url):
        return file_url.split('/')[-1]

    @staticmethod
    def get_storage_url(file_url):
        idx = file_url.rfind('/') + 1
        return file_url[:idx]

    @staticmethod
    def get_file_id(file_url):
        return file_url.split('_')[-1]
