from marshmallow import Schema, fields

from schemas.users.user_schema import UserSchema


class UserListSchema(Schema):
    users = fields.List(fields.Nested(UserSchema()))
