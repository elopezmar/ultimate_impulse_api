from flask import Blueprint
from flask_restful import Api

from resources.purchases.purchase_resource import PurchaseResource
from resources.purchases.purchase_list_resource import PurchaseListResource

purchase_blueprint = Blueprint('purchase', __name__)
api = Api(purchase_blueprint)

api.add_resource(PurchaseResource, '/purchase')
api.add_resource(PurchaseListResource, '/purchases')
