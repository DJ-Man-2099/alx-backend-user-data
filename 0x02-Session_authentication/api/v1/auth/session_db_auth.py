#!/usr/bin/env python3
""" Session Authentication Expiry DB Management Class """

from datetime import datetime, timedelta
from os import getenv
import uuid
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session Exp Auth Class """

    def create_session(self, user_id=None):
        """ that creates and stores new instance of UserSession
        and returns the Session ID"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
        user_session = UserSession(**kwargs)

        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """that returns the User ID
        by requesting UserSession in the database based on session_id"""

        if session_id is None:
            return None

        user_sessions = UserSession.search({"session_id": session_id})
        exp_user_id = super().user_id_for_session_id(session_id)
        if not user_sessions:
            return None
        if exp_user_id and exp_user_id == user_sessions[0].user_id:
            return user_sessions[0].user_id

        return None

    def destroy_session(self, request=None):
        """ that destroys the UserSession
        based on the Session ID from the request cookie """
        session_id = super().session_cookie(request)

        if not super().destroy_session(request):
            return False

        user_sessions = UserSession.search({"session_id": session_id})
        del user_sessions[0]
        return True
