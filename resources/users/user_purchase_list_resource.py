from flask_restful import Resource

from models.owners.owner import Owner
from models.purchases.purchase_list import PurchaseList
from schemas.purchases.purchase_list_schema import PurchaseListSchema
from resources.utils import handle_request


class UserPurchaseListResource(Resource):
    @handle_request()
    def get(self, user_id):
        schema = PurchaseListSchema(exclude=('purchases.owner',))
        owner = Owner(user_id).get()
        purchases = PurchaseList(owner=owner).get()
        return schema.dump(purchases.to_dict('purchases')), 200
