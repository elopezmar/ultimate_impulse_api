from gcp.storage import Storage
import uuid
from typing import Tuple
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from marshmallow import Schema, fields

from gcp.firestore import db

from schemas.common.exceptions import BusinessError
from schemas.common.security import Security

class SchemaTypes():
    FORUMS = {
        'schema_id': 'FORUMS',
        'schema_name': 'Forum',
        'collection_name': 'forums',
        'collection_pattern': 'forums/{}',
        'schema_owner_keys': ('id',)
    }
    FORUMS_TOPICS = {
        'schema_id': 'FORUMS_TOPICS',
        'schema_name': 'Topic',
        'collection_name': 'topics',
        'collection_pattern': 'forums/{}/topics/{}',
        'schema_owner_keys': ('id',)
    }
    FORUMS_TOPICS_REPLIES = {
        'schema_id': 'FORUMS_TOPICS_REPLIES',
        'schema_name': 'Reply',
        'collection_name': 'replies',
        'collection_pattern': 'forums/{}/topics/{}/replies/{}',
        'schema_owner_keys': ('id',)
    }
    IRS = {
        'schema_id': 'IRS',
        'schema_name': 'Ir',
        'collection_name': 'irs',
        'collection_pattern': 'irs/{}',
        'schema_owner_keys': ('owner', 'id')
    }
    IRS_SAMPLES = {
        'schema_id': 'IRS_SAMPLES',
        'schema_name': 'Sample',
        'collection_name': 'samples',
        'collection_pattern': 'irs/{}/samples/{}',
        'schema_owner_keys': ('owner',)
    }
    IRS_FILES = {
        'schema_id': 'IRS_FILES',
        'schema_name': 'File',
        'collection_name': 'files',
        'collection_pattern': 'irs/{}/files/{}',
        'schema_owner_keys': ('owner',)
    }
    IRS_REVIEWS = {
        'schema_id': 'IRS_REVIEWS',
        'schema_name': 'Review',
        'collection_name': 'reviews',
        'collection_pattern': 'irs/{}/reviews/{}',
        'schema_owner_keys': ('owner', 'id')
    }
    USERS = {
        'schema_id': 'USERS',
        'schema_name': 'User',
        'collection_name': 'users',
        'collection_pattern': 'users/{}',
        'schema_owner_keys': ('id',)
    }


class Handlers():
    class Methods():
        ALL = 'all'
        GET = 'get'
        SET = 'set'
        UPDATE = 'update'
        DELETE = 'delete'

        @classmethod
        def all(cls):
            return [cls.GET, cls.SET, cls.UPDATE, cls.DELETE]
    
    class Events():
        ON_START = 'on_start'
        ON_SUCCESS = 'on_success'
        ON_ERROR = 'on_error'

        @classmethod
        def all(cls):
            return [cls.ON_START, cls.ON_SUCCESS, cls.ON_ERROR]

    def __init__(self):
        self.method = None
        self.handlers = {}

        all_methods = Handlers.Methods.all()
        all_events = Handlers.Events.all()

        for method in all_methods:
            self.handlers[method] = {}
            for event in all_events:
                self.handlers[method][event] = []

    def add(self, method: str, event: str, func: callable):
        if method == self.Methods.ALL:
            for method in self.Methods.all():
                self.handlers[method][event].append(func)
        else:
            self.handlers[method][event].append(func)

    def execute(self, event: str, *args, **kwargs):
        if self.method:
            for handler in self.handlers[self.method][event]:
                handler(*args, **kwargs)
        

class DocumentSchema(Schema):
    id = fields.Str(required=True)

    def __init__(self, schema_type: dict, security: Security=Security(False), *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.schema_id = schema_type['schema_id']
        self.schema_name = schema_type['schema_name']
        self.collection_name = schema_type['collection_name']
        self.collection_pattern = schema_type['collection_pattern']
        self.schema_owner_keys = schema_type['schema_owner_keys']
        self.security = security
        self.storage = Storage(self.schema_name)
        self.handlers = Handlers()

    def get_document(self, document: dict, path_keys: Tuple=(), silent=False):
        self.handlers.method = Handlers.Methods.GET

        document_ref = self.get_document_ref(path_keys, document)
        document = self.document_to_dict(document_ref.get())

        if document:
            self.handlers.execute(Handlers.Events.ON_START, document, path_keys)
            self.handlers.execute(Handlers.Events.ON_SUCCESS, document, path_keys)
            return document

        if not silent:
            self.handlers.execute(Handlers.Events.ON_ERROR, document, path_keys)
            raise BusinessError(f'{self.schema_name} not found.', 404)
    
    def set_document(self, document: dict, path_keys: Tuple=()):
        self.handlers.method = Handlers.Methods.SET
        self.handlers.execute(Handlers.Events.ON_START, document, path_keys)

        document_ref = self.get_document_ref(path_keys, document)
        document_ref.set(document)
        document = self.document_to_dict(document_ref.get())

        self.handlers.execute(Handlers.Events.ON_SUCCESS, document, path_keys)
        return document

    def update_document(self, document: dict, path_keys: Tuple=(), silent=False):
        self.handlers.method = Handlers.Methods.UPDATE

        document_ref = self.get_document_ref(path_keys, document)
        old_document = self.document_to_dict(document_ref.get())

        if old_document:
            self.handlers.execute(Handlers.Events.ON_START, old_document, path_keys)

            document_ref.update(self.dict_to_dot_notation(document))
            document = self.document_to_dict(document_ref.get())

            self.handlers.execute(Handlers.Events.ON_SUCCESS, document, path_keys)
            return document

        if not silent:
            self.handlers.execute(Handlers.Events.ON_ERROR, document, path_keys)
            raise BusinessError(f'{self.schema_name} not found.', 404)

    def delete_document(self, document: dict, path_keys: Tuple=(), silent=False):
        self.handlers.method = Handlers.Methods.DELETE

        document_ref = self.get_document_ref(path_keys, document)
        document = self.document_to_dict(document_ref.get())

        if document:
            self.handlers.execute(Handlers.Events.ON_START, document, path_keys)
            document_ref.delete()
            self.handlers.execute(Handlers.Events.ON_SUCCESS, document, path_keys)
            return document

        if not silent:
            self.handlers.execute(Handlers.Events.ON_ERROR, document, path_keys)
            raise BusinessError(f'{self.schema_name} not found.', 404)

    def get_document_ref(self, path_keys: Tuple, document: dict):
        return db.document(
            self.collection_pattern.format(
                *path_keys, document.pop('id', uuid.uuid1().hex)
            )
        )

    @staticmethod
    def document_to_dict(document: DocumentSnapshot):
        if document.exists:
            return {'id': document.id, **document.to_dict()}
        return None

    @classmethod
    def dict_to_dot_notation(cls, d: dict, prefix=None):
        dic_doted = {}
        for k in d:
            if isinstance(d[k], dict):
                p = f'{prefix}.{k}' if prefix else k
                dic_doted.update(cls.dict_to_dot_notation(d[k], p))
            else:
                dic_doted[f'{prefix}.{k}' if prefix else k] = d[k]
        return dic_doted


class CollectionSchema(Schema):
    def __init__(self, 
            schema_type: dict,
            *args, **kwargs
        ):
        super().__init__(*args, **kwargs)
        
        self.schema_id = schema_type['schema_id']
        self.schema_name = schema_type['schema_name']
        self.collection_name = schema_type['collection_name']
        self.collection_pattern = schema_type['collection_pattern']
        self.schema_owner_keys = schema_type['schema_owner_keys']
        self.security = Security(False)
        self.handlers = Handlers()

    def get_documents(self, path_keys: Tuple=(), filters: list=[], to_list=False):
        self.handlers.method = Handlers.Methods.GET
        collection_ref = self.get_collection_ref(path_keys)
        
        for filter in filters:
            collection_ref = collection_ref.where(*filter)

        documents = self.documents_to_list(collection_ref.stream())
        self.handlers.execute(Handlers.Events.ON_SUCCESS, documents, path_keys)

        if not to_list:
            return self.documents_to_dict(documents)
        return documents

    def get_collection_ref(self, path_keys: Tuple=()):
        return db.collection(
            self.collection_pattern[:-3].format(*path_keys)
        )

    def documents_to_list(self, documents):
        return [{'id': doc.id, **doc.to_dict()} for doc in documents]

    def documents_to_dict(self, documents: list):
        return {self.collection_name: documents}
