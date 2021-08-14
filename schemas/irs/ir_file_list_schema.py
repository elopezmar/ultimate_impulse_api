from marshmallow import Schema, fields

from schemas.irs.ir_file_schema import IRFileSchema


class IRFileListSchema(Schema):
    files = fields.List(fields.Nested(IRFileSchema()))
