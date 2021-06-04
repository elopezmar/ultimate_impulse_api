from typing import Type
from flask_jwt_extended.utils import get_jwt_identity
from flask_restful import Resource, request

from gcp.storage import Storage

from schemas.common.base import DocumentSchema, SchemaTypes
from schemas.common.security import Security


class BaseResource(Resource):
    def __init__(self, schema: DocumentSchema, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = schema
        self.storage = Storage(self.schema.schema_id)
        self.security = Security()
        self.schema.security = self.security

    def __getattribute__(self, attr):
        method = object.__getattribute__(self, attr)
        if method and callable(method) and method.__name__ in ('post', 'get', 'put', 'delete'):
            self.security.method = method.__name__
        return method
    
    def load_request_data(self):
        self.json = request.get_json(silent=True)
        self.args = request.args

        try:
            user_id = get_jwt_identity()
            user_schema = DocumentSchema(SchemaTypes.USERS)
            self.security.set_requestor(user_schema.get_document(document={'id': user_id}))
        except RuntimeError:
            pass

        self.security.verify_privilege()
