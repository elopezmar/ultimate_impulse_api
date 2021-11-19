from flask import Blueprint
from flask_restful import Api

from resources.donations.donation_resource import DonationResource
from resources.donations.donation_list_resource import DonationListResource

donation_blueprint = Blueprint('donation', __name__)
api = Api(donation_blueprint)

api.add_resource(DonationResource, '/donation')
api.add_resource(DonationListResource, '/donations')
