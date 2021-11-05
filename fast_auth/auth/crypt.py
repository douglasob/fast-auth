from datetime import datetime, timedelta
from os import environ

from passlib.context import CryptContext

from fast_auth.models import User
from jose import jwt

# SECRET_KEY = environ['SECRET_KEY']
# TTL = int(environ.get('TTL_JWT', default=1440))
# ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'])


def create_token_jwt(user: User, extra_fields={}):
    ttl = int(environ.get('TTL_JWT', default=1440))
    data = {
        'exp': datetime.utcnow() + timedelta(minutes=ttl),
        'id': user.id,
        'name': user.username
    }

    data.update(extra_fields)

    token = jwt.encode(data, environ['SECRET_KEY'], 'HS256')
    return token


def decode_token_jwt(token: str):
    data = jwt.decode(token, environ['SECRET_KEY'], 'HS256')
    return data
