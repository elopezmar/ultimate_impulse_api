from flask_jwt_extended import jwt_required
from flask_restful import Resource, request

from models.donations.donation import Donation
from schemas.donations.donation import DonationSchema
from resources.utils import get_requestor, handle_errors


class DonationResource(Resource):
    @jwt_required()
    @handle_errors()
    def post(self):
        schema = DonationSchema(partial=('id',))
        data = schema.load(request.get_json())
        donation = Donation().from_dict(data)
        donation.set(get_requestor())
        return schema.dump(donation.to_dict()), 201

    @handle_errors()
    def get(self):
        schema = DonationSchema()
        donation = Donation(id=request.args['id']).get()
        return schema.dump(donation.to_dict()), 200

    @jwt_required()
    @handle_errors()
    def delete(self):
        schema = DonationSchema(partial=('amount',), only=('id',))
        data = schema.load(request.get_json())
        donation = Donation().from_dict(data)
        donation.delete(get_requestor())
        return {'message': 'Donation deleted.'}, 200
