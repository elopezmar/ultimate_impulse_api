from marshmallow import Schema, fields


class FileSchema(Schema):
    url = fields.Str(required=True)
    b64_data = fields.Str(required=True, load_only=True)
