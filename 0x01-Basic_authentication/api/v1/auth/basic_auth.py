#!/usr/bin/env python3
""" Basic Authentication Management Class """

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth Class """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization header
        for a Basic Authentication """
        if not (authorization_header
                and isinstance(authorization_header, str)
                and authorization_header.startswith("Basic ")):
            return None
        return authorization_header[6:]

    # def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
    #     """ returns False """
    #     if path and path[-1] != "/":
    #         path += "/"

    #     return path is None \
    #         or not excluded_paths \
    #         or not (path in excluded_paths)

    # def authorization_header(self, request=None) -> str:
    #     """ returns None """
    #     HEADER = 'Authorization'
    #     if not request:
    #         return None
    #     return request.headers.get(HEADER)

    # def current_user(self, request=None) -> User:
    #     """ returns None """
    #     return None