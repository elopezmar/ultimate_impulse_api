import functools

from marshmallow.exceptions import ValidationError
from flask_jwt_extended import get_jwt_identity
from flask_restful import request

from models.users.user import User
from models.exceptions import BusinessError

def get_bool_arg(name: str) -> bool:
    return request.args.get(name, '').lower() == 'true'

def get_requestor() -> User:
    try:
        user = User(id=get_jwt_identity()).get()
    except RuntimeError:
        user = User()
    except BusinessError:
        user = User()
    return user

def handle_errors():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidationError as err:
                return err.messages, 400
            except BusinessError as err:
                return err.message
            except KeyError as err:
                return {'message': 'An id must be provided as parameter.'}, 400
        return wrapper
    return decorator