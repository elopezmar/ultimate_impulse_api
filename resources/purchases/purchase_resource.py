from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.irs.ir import IR
from models.purchases.purchase import Purchase
from schemas.purchases.purchase_schema import PurchaseSchema
from resources.utils import get_bool_arg, handle_request


class PurchaseResource(Resource):
    @jwt_required()
    @handle_request()
    def post(self):
        schema = PurchaseSchema(partial=('id', 'ir.title',))
        data = schema.load(request.get_json())
        ir = IR(id=data['ir']['id']).get()
        purchase = Purchase(ir=ir).set()
        return schema.dump(purchase.to_dict()), 201

    @handle_request()
    def get(self):
        schema = PurchaseSchema()
        purchase = Purchase(id=request.args['id']).get(
            ir_files=get_bool_arg('ir-files')
        )
        return schema.dump(purchase.to_dict()), 200

    @jwt_required()
    @handle_request()
    def delete(self):
        schema = PurchaseSchema(partial=('ir',), only=('id',))
        data = schema.load(request.get_json())
        purchase = Purchase(id=data['id']).get()
        purchase.delete()
        return {'message': 'Purchase deleted.'}, 200
