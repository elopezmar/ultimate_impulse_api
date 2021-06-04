from datetime import datetime
from statistics import mean
from marshmallow import fields, validate
from google.api_core.exceptions import NotFound

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

    # @classmethod
    # def uptade_stats(cls, ir_id):
    #     try:
    #         reviews = IRReviewsSchema().read_list(ir_id)

    #         ir_ref = db.document(cls.get_document_path(ir_id))
    #         ir_ref.update({
    #             'stats.reviews': len(reviews),
    #             'stats.rating': mean([review['rating'] for review in reviews])
    #         })
    #     except NotFound:
    #         raise BusinessError('IR not found.', 404)
