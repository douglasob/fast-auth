import asyncio
import os
from datetime import datetime
from getpass import getpass

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fast_auth.database import get_session
from fast_auth.models import User
from sqlalchemy import select

from .crypt import decode_token_jwt, pwd_context

oauth2_scheme = OAuth2PasswordBearer('/login')


def get_token_payload(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token_jwt(token)
        del payload['exp']
        return payload
    except:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception


async def get_user_groups(user: User):
    query = '''
        select ag.id, ag.name
            from auth_groups ag
                inner join auth_users_groups aug on aug.auth_group_id = ag.id
            where aug.auth_user_id = :user_id
    '''

    async with get_session() as session:
        groups = await session.execute(query, {'user_id': user.id})
        dict_groups = [dict(g) for g in groups]
        return dict_groups


async def authenticate(username, password) -> User:
    stmt_user = select(User).where(User.username == username).limit(1)

    async with get_session() as session:
        user = await session.execute(stmt_user)
        user = user.scalar()

        if user:
            checked = pwd_context.verify(password, user.password)

            if checked:
                user.last_login = datetime.now()
                await session.commit()

                return user


async def _create_user(user: User):
    async with get_session() as session:
        session.add(user)
        await session .commit()


def create_user_cli():
    from fast_auth.database import connect
    engine, _ = connect()

    os_user = os.getlogin()
    print('')
    username = input(f'Username [{os_user}]: ')
    username = username if username else os_user
    password = getpass()

    user = User()
    user.username = username
    user.password = password
    user.created_at = datetime.now()

    asyncio.run(_create_user(user))
