from werkzeug.exceptions import HTTPException


class BusinessError(Exception):
    def __init__(self, status, message):
        self.message = {'msg': message}, status


class ModelError(HTTPException):
    errors = {}

    def __init__(self, error_code=None, description=None, response=None):
        super().__init__(description=description, response=response)


class DonationError(ModelError):
    errors = {
        2010001: (400, 'Donations only can be deleted by admin users')
    }


class ForumError(ModelError):
    errors = {
        3010001: (400, 'Forums only can be created by admin users'),
        3010002: (400, 'Forums only can be updated by admin users'),
        3010003: (400, 'Forums only can be deleted by admin users'),
        3020001: (400, 'Forum Topics only can be created by logged in users'),
        3020002: (400, 'Forum Topics only can be updated by the owner or admin users'),
        3020003: (400, 'Forum Topics only can be deleted by the owner or admin users'),
        3030001: (400, 'Forum Replies only can be created by logged in users'),
        3030002: (400, 'Forum Replies only can be updated by the owner or admin users'),
        3030003: (400, 'Forum Replies only can be deleted by the owner or admin users'),
    }
    

class IRError(ModelError):
    errors = {
        4010001: (400, 'IRs only can be created by collaborators or admin users'),
        4010002: (400, 'IRs only can be updated by the owner or admin users'),
        4010003: (400, 'IRs only can be deleted by the owner or admin users'),
        4020001: (400, 'IR Samples only can be created by the IR owner or admin users'),
        4020002: (400, 'IR Samples only can be updated by the IR owner or admin users'),
        4020003: (400, 'IR Samples only can be deleted by the IR owner or admin users'),
        4030001: (400, 'IR Files only can be created by the IR owner or admin users'),
        4030002: (400, 'IR Files only can be updated by the IR owner or admin users'),
        4030003: (400, 'IR Files only can be deleted by the IR owner or admin users'),
        4040001: (400, 'IR Reviews only can be created by logged in users'),
        4040002: (400, 'IR Reviews only can be updated by the owner or admin users'),
        4040003: (400, 'IR Reviews only can be deleted by the owner or admin users'),
        4040004: (400, 'IR Review not belong to the IR'),
    }


class PurchaseError(ModelError):
    errors = {
        5010001: (400, 'Purchases only can be created by logged in users'),
        5010002: (400, 'Purchases only can be updated by the owner or admin users'),
        5010003: (400, 'Purchases only can be deleted by the owner or admin users'),
    }


class ReviewError(ModelError):
    errors = {
        6010001: (400, 'Reviews only can be created by collaborators or admin users'),
        6010002: (400, 'Reviews only can be updated by the owner or admin users'),
        6010003: (400, 'Reviews only can be deleted by the owner or admin users'),
        6020001: (400, 'Review content only can be created by the review owner or admin users'),
        6020002: (400, 'Review content only can be updated by the review owner owner or admin users'),
        6020003: (400, 'Review content only can be deleted by the review owner owner or admin users'),
        6020004: (404, 'Review content not found'),
        6030001: (400, 'Review comments only can be created by logged in users'),
        6030002: (400, 'Review comments only can be updated by the owner or admin users'),
        6030003: (400, 'Review comments only can be deleted by the owner or admin users'),
        6030004: (400, 'Review comment not belong to the review'),
    }


class UserError(ModelError):
    errors = {
        7010001: (400, 'Invalid user role'),
        7010002: (400, 'Only admin users can create collaborators or admin users'),
        7010003: (400, 'Email already exists'),
        7010001: (400, 'Username already exists'),
        7010002: (400, 'Users only can be updated by the owner or admin users'),
        7010003: (400, 'Old password is incorrect'),
        7010004: (404, 'New password cannot be old password'),
        7010001: (400, 'Users only can be deleted by the owner or admin users'),
        7010002: (400, 'User not verified'),
        7010003: (400, 'Invalid email or password'),
        7010004: (404, 'User not found'),
    }