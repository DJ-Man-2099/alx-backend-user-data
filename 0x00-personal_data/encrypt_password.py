#!/usr/bin/env python3
"""Second Task"""

import bcrypt


def hash_password(password: str) -> str:
    """function that takes a password string
    and returns a hashed password string"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
