from marshmallow import Schema, fields

from schemas.irs.ir_schema import IRSchema
from schemas.owners.owner_schema import OwnerSchema


class PurchaseSchema(Schema):
    id = fields.Str(required=True)
    ir = fields.Nested(IRSchema(only=('id', 'title', 'description')))
    owner = fields.Nested(OwnerSchema(), dump_only=True)
    purchased_at = fields.DateTime(dump_only=True)
    total = fields.Float(dump_only=True)
