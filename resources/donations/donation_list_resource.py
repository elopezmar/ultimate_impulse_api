from flask_restful import Resource

from models.donations.donation_list import DonationList
from schemas.donations.donation import DonationSchema
from resources.utils import handle_request


class DonationListResource(Resource):
    @handle_request()
    def get(self):
        schema = DonationSchema(many=True)
        donations = DonationList().get()
        return {'donations': schema.dump(donations.to_list())}, 200
