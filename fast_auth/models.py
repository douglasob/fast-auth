from typing import Any
from sqlalchemy import Column, FetchedValue, ForeignKey, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import Boolean

Base = declarative_base()


class User(Base):

    __tablename__ = 'auth_users'

    id = Column(Integer, primary_key=True, autoincrement=True,
                server_default=FetchedValue())
    username = Column(Text, unique=True)
    email = Column(Text)
    name = Column(Text)
    password = Column(Text)
    created_at = Column(DateTime)
    last_login = Column(DateTime)
    enable = Column(Boolean, default=True)

    def __setattr__(self, name: str, value: Any) -> None:
        from fast_auth.auth.crypt import pwd_context

        if name == 'password':
            super().__setattr__(name, pwd_context.hash(value))
        else:
            super().__setattr__(name, value)


class Group(Base):

    __tablename__ = 'auth_groups'

    id = Column(Integer, primary_key=True, autoincrement=True,
                server_default=FetchedValue())
    name = Column(Text)


class UserGroup(Base):

    __tablename__ = 'auth_users_groups'

    id = Column(Integer, primary_key=True, autoincrement=True,
                server_default=FetchedValue())
    auth_user_id = Column(Integer, ForeignKey('auth_users.id'))
    auth_group_id = Column(Integer, ForeignKey('auth_groups.id'))
