from __future__ import annotations
import datetime
import uuid

import google.auth
from google.auth import compute_engine
from google.auth.transport import requests

from cloud_storage.client import client


class File():
    BUCKET_NAME = 'storage-ui-dev'

    def __init__(self, prefix: str='temp', url: str=None):
        if url:
            self.name = url.split('/')[-1].split('?')[0]
        else:
            self.name = f'{prefix}_{uuid.uuid1().hex}'

        self.bucket = client.bucket(self.BUCKET_NAME)
        self.blob = self.bucket.blob(self.name)
        self.url = self.blob.public_url

    @property
    def signed_url(self) -> str:
        credentials, _ = google.auth.default()
        if not hasattr(credentials, 'signer_email'):
            '''
                # Se debe de agragar el rol Service Account Token Creator a la 
                # cuenta de servicion default del AppEngine. 
                # Por ejemplo: ultimate-impulse-dev@appspot.gserviceaccount.com
            '''
            request = requests.Request()
            credentials = compute_engine.IDTokenCredentials(request, '')

        return self.blob.generate_signed_url(
            version='v4',
            expiration=datetime.timedelta(minutes=15),
            method='GET',
            credentials=credentials
        )

    @property
    def is_temp(self) -> bool:
        return self.name.startswith('temp_')

    def upload(self, data: bytes) -> File:
        self.blob.upload_from_string(data)
        return self

    def delete(self):
        if self.blob.exists():
            self.blob.delete()
        
    def overwrite(self, data: File) -> File:
        if self.name == data.name:
            return 
        if not data.blob.exists():
            raise f'File {data.url} does not exists.'
        if self.blob.exists():
            self.blob.delete()

        self.blob = self.bucket.rename_blob(data.blob, self.name)
        return self

    def accessibility(self, public: bool) -> File:
        if public:
            self.blob.make_public()
        return self
    
        

        
        

