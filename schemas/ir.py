from datetime import datetime
from gcp.storage import Storage
from statistics import mean
from marshmallow import fields, validate

from schemas.common.base import CollectionSchema, DocumentSchema, SchemaTypes


class IRSampleSchema(DocumentSchema):
    title = fields.Str(required=True)
    description = fields.Str()
    file_url = fields.Url(required=True)
    owner = fields.Str(dump_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(SchemaTypes.IRS_SAMPLES, *args, **kwargs)

    def set_owner(self, document: dict):
        document['owner'] = self.security.requestor['id']
        return document


class IRFileSchema(DocumentSchema):
    title = fields.Str(required=True)
    description = fields.Str()
    file_url = fields.Url(required=True)
    owner = fields.Str(dump_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(SchemaTypes.IRS_FILES, *args, **kwargs)

    def set_owner(self, document: dict):
        document['owner'] = self.security.requestor['id']
        return document

    def manage_file(self, document: dict, ir: dict):
        requestor_id = self.security.requestor.get('id')
        premium = ir.get('premium', False)
        if premium:
            if requestor_id:
                document['file_url'] = Storage().get_signed_url(
                    document['file_url']
                )
            else:
                document.pop('file_url')
        return document


class IRReviewSchema(DocumentSchema):
    USER_FIELDS = ('id', 'username', 'profile.country', 'profile.social_media')

    title = fields.Str(required=True)
    description = fields.Str()
    rating = fields.Float(required=True, validate=validate.Range(min=0, max=5))
    likes = fields.Integer(dump_only=True)
    created_at = fields.DateTime(missing=datetime.now())
    owner = fields.Dict(dump_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(SchemaTypes.IRS_REVIEWS, *args, **kwargs)

    def set_owner(self, document: dict):
        requestor = self.security.requestor
        document['owner'] = {
            'id': requestor['id'],
            'username': requestor['username'],
            'profile': {
                'country': requestor.get('country'),
                'social_media': requestor.get('social_media', [])
            }
        }
        return document


class IRSamplesSchema(CollectionSchema):
    samples = fields.List(fields.Nested(IRSampleSchema()))

    def __init__(self, *args, **kwargs):
        super().__init__(SchemaTypes.IRS_SAMPLES, *args, **kwargs)


class IRFilesSchema(CollectionSchema):
    files = fields.List(fields.Nested(IRFileSchema()))

    def __init__(self, *args, **kwargs):
        super().__init__(SchemaTypes.IRS_FILES, *args, **kwargs)

    def manage_files(self, documents: dict, ir: dict):
        ir_file_schema = IRFileSchema()
        ir_file_schema.security = self.security

        for file in documents[self.collection_name]:
            file = ir_file_schema.manage_file(file, ir)

        return documents


class IRReviewsSchema(CollectionSchema):
    reviews = fields.List(fields.Nested(IRReviewSchema()))

    def __init__(self, *args, **kwargs):
        super().__init__(SchemaTypes.IRS_REVIEWS, *args, **kwargs)
        

class IRSchema(DocumentSchema):
    title = fields.Str(required=True)
    description = fields.Str()
    published_at = fields.DateTime(missing=datetime.now())
    owner = fields.Dict(dump_only=True)
    pics_urls = fields.List(fields.Url())
    premium = fields.Boolean(missing=False)
    samples = fields.List(fields.Nested(IRSampleSchema()))
    files = fields.List(fields.Nested(IRFileSchema()))
    reviews = fields.List(fields.Nested(IRReviewSchema()), dump_only=True)
    stats = fields.Dict(
        reviews = fields.Integer(dump_only=True),
        rating = fields.Float(dump_only=True)
    ) 

    def __init__(self, *args, **kwargs):
        super().__init__(SchemaTypes.IRS, *args, **kwargs)

    def set_owner(self, document: dict):
        requestor = self.security.requestor
        document['owner'] = {
            'id': requestor['id'],
            'username': requestor['username'],
            'profile': {
                'country': requestor.get('country'),
                'social_media': requestor.get('social_media', [])
            }
        }
        return document

    def update_stats(self, ir_id):
        reviews = IRReviewsSchema().get_documents((ir_id,), to_list=True)
        ir = {
            'id': ir_id,
            'stats': {
                'reviews': len(reviews),
                'rating': mean([review['rating'] for review in reviews])
            }
        }
        self.update_document(ir)


class IRsSchema(CollectionSchema):
    irs = fields.List(fields.Nested(IRSchema()))

    def __init__(self, *args, **kwargs):
        super().__init__(SchemaTypes.IRS, *args, **kwargs)

