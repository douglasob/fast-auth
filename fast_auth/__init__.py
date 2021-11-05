__version__ = '0.1.0'

from .database import get_db
from .database import connect as connect_database
from .auth.crypt import create_token_jwt
from .auth.auth import get_token_payload as require_auth
from .auth.auth import authenticate

import logging
from os import path, environ
from dotenv import load_dotenv

current_dir = path.abspath(path.curdir)
env_file = path.join(current_dir, '.env')
load_dotenv(env_file)

if 'SECRET_KEY' not in environ:
    logging.warning(
        '\033[93mSECRET_KEY not found in environment variables!\033[93m')
