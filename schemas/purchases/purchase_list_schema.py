from marshmallow import Schema, fields

from schemas.purchases.purchase_schema import PurchaseSchema


class PurchaseListSchema(Schema):
    purchases = fields.List(fields.Nested(PurchaseSchema()))
