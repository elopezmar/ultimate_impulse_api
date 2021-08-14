from marshmallow import Schema, fields

from schemas.irs.ir_schema import IRSchema


class IRListSchema(Schema):
    irs = fields.List(fields.Nested(IRSchema()))
