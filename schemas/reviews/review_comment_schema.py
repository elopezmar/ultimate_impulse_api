from marshmallow import Schema, fields

from schemas.owners.owner_schema import OwnerSchema


class ReviewCommentSchema(Schema):
    id = fields.Str(required=True)
    description = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    owner = fields.Nested(OwnerSchema(), dump_only=True)
    