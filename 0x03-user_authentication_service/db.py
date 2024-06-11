#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.session = DBSession()
        return self.session

    def add_user(self, email: str, hashed_password: str) -> User:
        """add a new user to the db"""
        if not email or not hashed_password:
            raise InvalidRequestError
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user
