from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.purchases.purchase import Purchase
from schemas.purchases.purchase_schema import PurchaseSchema
from resources.utils import get_requestor, handle_errors


class PurchaseResource(Resource):
    @jwt_required()
    @handle_errors()
    def post(self):
        schema = PurchaseSchema(partial=('id', 'ir.title',))
        data = schema.load(request.get_json())
        ir = IR(id=data['ir']['id']).get()
        purchase = Purchase(ir=ir).set(get_requestor())
        return schema.dump(purchase.to_dict()), 201

    @handle_errors()
    def get(self):
        schema = PurchaseSchema()
        purchase = Purchase(id=request.args['id']).get()
        return schema.dump(purchase.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def delete(self):
        schema = PurchaseSchema(partial=('ir',), only=('id',))
        data = schema.load(request.get_json())
        purchase = Purchase().from_dict(data)
        purchase.delete(get_requestor())
        return {'message': 'Purchase deleted.'}, 200
