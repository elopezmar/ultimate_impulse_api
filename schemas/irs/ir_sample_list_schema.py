from marshmallow import Schema, fields

from schemas.irs.ir_sample_schema import IRSampleSchema


class IRSampleListSchema(Schema):
    samples = fields.List(fields.Nested(IRSampleSchema()))
