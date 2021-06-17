import uuid
from typing import Tuple
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from marshmallow import Schema, fields
from marshmallow.fields import List

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


class DocumentSchema(Schema):
    id = fields.Str(required=True)

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

    def get_document(self, document: dict, collection_path_ids: Tuple=(), silent=False):
        document_path_ids = (*collection_path_ids, document['id'])
        document = self.get_document_ref(document_path_ids).get()
        if document.exists:
            document = self.document_to_dict(document)
            self.security_validations(document)
            return document
        if not silent:
            raise BusinessError(f'{self.schema_name} not found.', 404)
    
    def set_document(self, document: dict, collection_path_ids: Tuple=()):
        self.security_validations(document)
        document_id = self.get_new_document_id()
        document_path_ids = (*collection_path_ids, document_id)
        self.get_document_ref(document_path_ids).set(document)
        document['id'] = document_id
        return document

    def update_document(self, document: dict, collection_path_ids: Tuple=(), silent=False):
        document_path_ids = (*collection_path_ids, document['id'])
        document_ref = self.get_document_ref(document_path_ids)
        current_document = document_ref.get()
        if current_document.exists:
            current_document = self.document_to_dict(current_document)
            self.security_validations(current_document)
            document.pop('id')
            document = self.dict_to_dot_notation(document)
            document_ref.update(document)
            return self.document_to_dict(document_ref.get())
        if not silent:
            raise BusinessError(f'{self.schema_name} not found.', 404)

    def delete_document(self, document: dict, collection_path_ids: Tuple=(), silent=False):
        document_path_ids = (*collection_path_ids, document['id'])
        document_ref = self.get_document_ref(document_path_ids)
        document = document_ref.get()
        if document.exists:
            document = self.document_to_dict(document)
            self.security_validations(document)
            document_ref.delete()
            return document
        if not silent:
            raise BusinessError(f'{self.schema_name} not found.', 404)

    def security_validations(self, document: dict):
        owner_id = self.get_document_owner_id(document)
        self.security.verify_ownership(owner_id)

    def get_document_ref(self, document_path_ids: Tuple):
        document_path = self.get_document_path(document_path_ids)
        return db.document(document_path)

    def get_document_path(self, document_path_ids: Tuple):
        return self.collection_pattern.format(*document_path_ids)

    def get_document_owner_id(self, document: dict):
        try:
            owner_id = None
            for key in self.schema_owner_keys:
                if owner_id == None:
                    owner_id = document[key]
                else:
                    owner_id = owner_id[key]
            return owner_id
        except KeyError:
            return None

    @staticmethod
    def get_new_document_id():
        return uuid.uuid1().hex

    @staticmethod
    def document_to_dict(document: DocumentSnapshot):
        if document.exists:
            return {'id': document.id, **document.to_dict()}
        return None

    @classmethod
    def dict_to_dot_notation(cls, d, prefix=None):
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

    def get_documents(self, collection_path_ids: Tuple=(), filters: List=[], to_list=False):
        collection_ref = self.get_collection_ref(collection_path_ids)
        
        for filter in filters:
            collection_ref = collection_ref.where(*filter)
        documents = collection_ref.stream()

        if to_list:
            return self.documents_to_list(documents)
        return self.documents_to_dict(documents)

    def get_collection_path(self, collection_path_ids: Tuple=()):
        return self.collection_pattern[:-3].format(*collection_path_ids)
        
    def get_collection_ref(self, collection_path_ids: Tuple=()):
        collection_path = self.get_collection_path(collection_path_ids)
        return db.collection(collection_path)

    def documents_to_list(self, documents):
        return [{'id': doc.id, **doc.to_dict()} for doc in documents]

    def documents_to_dict(self, documents):
        return {self.collection_name: self.documents_to_list(documents)}
        