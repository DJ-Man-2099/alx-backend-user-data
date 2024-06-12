#!/usr/bin/env python3
""" Auth module """

import uuid
import bcrypt
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from db import DB, User


def _hash_password(password: str) -> str:
    """ Returns a hashed password """

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ Returns a string representation of a new UUID """

    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a new user and saves it to the database.
        """
        if not (email and password):
            raise InvalidRequestError

        try:
            already_exists = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """ Try locating the user by email.
        If it exists, check the password with bcrypt.checkpw.
        If it matches return True. In any other case, return False """

        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """  takes an email string argument
        and returns the session ID as a string """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db.session.commit()
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ If the session ID is None or no user is found, return None.
        Otherwise return the corresponding user. """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int):
        """  updates the corresponding user’s session ID to None. """
        if user_id is None:
            return None

        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None
