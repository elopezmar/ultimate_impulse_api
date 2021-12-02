import functools

from google.api_core.exceptions import NotFound
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import get_jwt_identity
from flask_restful import request

from firestore.cache import cache
from models.exceptions import BusinessError
from resources.session import requestor

def get_bool_arg(name: str) -> bool:
    return request.args.get(name, '').lower() == 'true'

def set_requestor():
    try:
        requestor.get(get_jwt_identity())
    except RuntimeError:
        requestor.reset()
    except BusinessError:
        requestor.reset()

def handle_request():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                cache.clear()
                set_requestor()
                return func(*args, **kwargs)
            except ValidationError as err:
                return err.messages, 400
            except BusinessError as err:
                return err.message
            except NotFound as err:
                return err.message, 404
            except KeyError as err:
                return {'message': 'An id must be provided as parameter.'}, 400
        return wrapper
    return decorator
