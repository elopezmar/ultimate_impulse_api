from marshmallow import Schema, fields


class IRSampleSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    file_url = fields.Url(required=True)
