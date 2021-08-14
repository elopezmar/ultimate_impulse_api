from datetime import datetime

from marshmallow import Schema, fields

from models.utils import Roles


class UserSchema(Schema):
    id = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    username = fields.Str(required=True)
    created_at = fields.DateTime(missing=datetime.now())
    verified = fields.Boolean(dump_only=True)
    role = fields.Str(missing=Roles.USER)
    profile = fields.Nested(Schema.from_dict(dict(
        first_name = fields.Str(),
        last_name = fields.Str(),
        born = fields.Date(),
        country = fields.Str(),
        pic_url = fields.Url(),
        social_media = fields.List(fields.Url())
    )))
    stats = fields.Nested(Schema.from_dict(dict(
        topics_created = fields.Number()
    )))
    old_password = fields.Str(load_only=True)
    new_password = fields.Str(load_only=True)
