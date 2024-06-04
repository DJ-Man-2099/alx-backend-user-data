#!/usr/bin/env python3
""" Authentication Management Class """

import re
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    """ Auth Class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False """
        if path and path[-1] != "/":
            path += "/"

        return path is None \
            or not excluded_paths \
            or not any(map(lambda p: not not re.match(p, path),
                           excluded_paths))

    def authorization_header(self, request=None) -> str:
        """ returns None """
        HEADER = 'Authorization'
        if not request:
            return None
        return request.headers.get(HEADER)

    def current_user(self, request=None) -> User:
        """ returns None """
        return None
