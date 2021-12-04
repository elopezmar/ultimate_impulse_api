from flask_restful import Resource, request

from models.irs.ir import IR
from models.owners.owner import Owner
from models.purchases.purchase_list import PurchaseList
from schemas.purchases.purchase_list_schema import PurchaseListSchema
from resources.utils import handle_request


class PurchaseListResource(Resource):
    @handle_request()
    def get(self):
        schema = PurchaseListSchema()

        id = request.args.get('ir_id')
        ir = IR(id).get() if id else None

        id = request.args.get('user_id')
        owner = Owner(id).get() if id else None

        purchases = PurchaseList(ir=ir, owner=owner).get()
        return schema.dump(purchases.to_dict('purchases')), 200
