from marshmallow import Schema, fields

class ReviewSectionSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str()
    description = fields.Str()
    pic_url = fields.Url()
    youtube_links = fields.List(fields.Url())
    