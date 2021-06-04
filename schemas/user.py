from datetime import datetime
from marshmallow import Schema, fields

from schemas.common.base import DocumentSchema, CollectionSchema, SchemaTypes


class UserSchema(DocumentSchema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    username = fields.Str(required=True)
    created_at = fields.DateTime(missing=datetime.now())
    verified = fields.Boolean(dump_only=True)
    role = fields.Str(dump_only=True)
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

    #Aux fields for update
    old_password = fields.Str(load_only=True)
    new_password = fields.Str(load_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(SchemaTypes.USERS, *args, **kwargs)
        

class UsersSchema(CollectionSchema):
    users = fields.List(fields.Nested(UserSchema()))

    def __init__(self, *args, **kwargs):
        super().__init__(SchemaTypes.USERS, *args, **kwargs)
