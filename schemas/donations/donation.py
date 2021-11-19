from marshmallow import Schema, fields

from schemas.owners.owner_schema import OwnerSchema


class DonationSchema(Schema):
    id = fields.Str(required=True)
    owner = fields.Nested(OwnerSchema(), dump_only=True)
    amount = fields.Float(required=True)
    created_at = fields.DateTime(dump_only=True)
