from marshmallow import Schema, fields, validate

from schemas.owners.owner_schema import OwnerSchema


class IRReviewSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    rating = fields.Float(required=True, validate=validate.Range(min=0, max=5))
    likes = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    owner = fields.Nested(OwnerSchema(), dump_only=True)
