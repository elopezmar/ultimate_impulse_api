from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.donations.donation_list import DonationList
from schemas.donations.donation import DonationSchema
from resources.utils import get_requestor, handle_errors


class DonationListResource(Resource):
    @handle_errors()
    def get(self):
        schema = DonationSchema(many=True)
        donations = DonationList().get()
        return {'donations': schema.dump(donations.to_list())}, 200
