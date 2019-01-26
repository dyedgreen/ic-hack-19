"""
Functions on reasons / apps
exposed to api
"""

from . import user
from . import reason

def get(token, uri):
    usr = user.User.from_session(token)
    app = reason.App(uri, usr)
    if not app.exists:
        raise ValueError("App does not exist")
    return app

def create(token, uri, name, icon):
    usr = user.User.from_session(token)
    return reason.App.create(uri, usr, name, icon)

def list(token, uri):
    usr = user.User.from_session(token)
    app = reason.App(uri, usr)
    return app.reasons

def add_reason(token, uri, reason_str):
    usr = user.User.from_session(token)
    reason.App(uri, usr).add_reason(reason_str)
