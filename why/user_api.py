"""
Functions on users exposed
to api
"""

import re

from . import user as u


def create(username, password):
    # Validate
    if not re.match("^[a-zA-Z0-9_\\-.]{1,64}$", username):
        raise ValueError("Username invalid")
    if len(password) < 6:
        raise ValueError("The password has to be at least 6 characters long")
    user = u.User(username)
    if user.exists:
        raise ValueError("User already exists")
    user.create(password)
    return user

def login(app_name, username, password):
    user = u.User(username)
    if not user.exists:
        raise ValueError("User does not exist")
    if not user.authenticate(password):
        raise ValueError("Invalid password")
    return user.create_session(app_name)

def logout(token):
    try:
        user = u.User.from_session(token)
        user.destroy_session(token)
    except:
        pass

def update_password(username, password, new_password):
    if len(new_password) < 6:
        raise ValueError("The password has to be at least 6 characters long")
    user = u.User(username)
    if not user.authenticate(password):
        raise ValueError("Invalid password")
    user.update_password(new_password)
