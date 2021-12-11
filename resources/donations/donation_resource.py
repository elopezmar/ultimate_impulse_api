from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.donations.donation import Donation
from schemas.donations.donation import DonationSchema
from resources.utils import handle_request


class DonationResource(Resource):
    @jwt_required()
    @handle_request()
    def post(self):
        schema = DonationSchema(partial=('id',))
        data = schema.load(request.get_json())
        donation = Donation().from_dict(data)
        donation.set()
        return schema.dump(donation.to_dict()), 201

    @handle_request()
    def get(self):
        schema = DonationSchema()
        donation = Donation(id=request.args['id']).get()
        return schema.dump(donation.to_dict()), 200

    @jwt_required()
    @handle_request()
    def delete(self):
        schema = DonationSchema(partial=('amount',), only=('id',))
        data = schema.load(request.get_json())
        donation = Donation(id=data['id']).get()
        donation.delete()
        return {'message': 'Donation deleted.'}, 200
