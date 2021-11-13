from __future__ import annotations

from marshmallow import Schema, fields


class OwnerSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    profile = fields.Nested(Schema.from_dict(dict(
        country = fields.Str(),
        pic_url = fields.Url(),
        social_media = fields.List(fields.Url())
    )))
