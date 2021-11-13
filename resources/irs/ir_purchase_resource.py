from flask_restful import Resource

from models.irs.ir import IR
from models.purchases.purchase_list import PurchaseList
from schemas.purchases.purchase_list_schema import PurchaseListSchema
from resources.utils import handle_errors


class IRPurchaseListResource(Resource):
    @handle_errors()
    def get(self, ir_id):
        schema = PurchaseListSchema(exclude=('purchases.ir',))
        ir = IR(ir_id).get()
        purchases = PurchaseList(ir=ir).get()
        return schema.dump(purchases.to_dict('purchases')), 200
