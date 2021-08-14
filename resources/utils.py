from flask_jwt_extended import get_jwt_identity
from models.users.user import User

def get_requestor() -> User:
    try:
        user = User(id=get_jwt_identity()).get()
    except RuntimeError:
        user = User()
    return user