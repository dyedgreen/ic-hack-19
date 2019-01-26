"""
Manage users and their
login sessions / apps
"""

import hashlib
import random
import time

from . import db


class User:

    def __init__(self, username, password=None):
        self._username = str(username)
        self._id = None

        if password is not None:
            self.create(password)

        # Load id from db
        c = db.conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? LIMIT 1", [self._username])
        self._id = c.fetchone()
        if self._id:
            self._id = int(self._id[0])

    def from_session(token):
        c = db.conn.cursor()
        c.execute(
            "SELECT username FROM users WHERE id=(SELECT user FROM sessions WHERE token=? LIMIT 1) LIMIT 1",
            [token])
        username = c.fetchone()
        if not username:
            raise ValueError("Session does not exists")
        return User(username[0])

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def exists(self):
        return self._id is not None

    @property
    def sessions(self):
        c = db.conn.cursor()
        c.execute(
            "SELECT name, token, created FROM sessions WHERE user=?",
            [self.id])
        sess_list = []
        for row in c:
            sess_list.append(Session(self, *row))
        return sess_list

    def create(self, password):
        salt = User.salt()
        c = db.conn.cursor()
        c.execute(
            "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
            [self._username, User.hash(password, salt), salt])
        db.conn.commit()

    def update_password(self, new_pass):
        salt = User.salt()
        c = db.conn.cursor()
        c.execute(
            "UPDATE users SET password=?, salt=? WHERE username=?",
            [User.hash(new_pass, salt), salt, self._username])
        db.conn.commit()

    def create_session(self, name):
        if not self.exists:
            raise ValueError("User {} does not exists".format(self.username))
        token = User.salt(128)
        c = db.conn.cursor()
        c.execute(
            "INSERT INTO sessions (user, name, token, created) VALUES(?,?,?,?)",
            [self.id, str(name), token, time.time()])
        db.conn.commit()
        return token

    def destroy_session(self, token):
        if not self.exists:
            raise ValueError("User {} does not exists".format(self.username))
        c = db.conn.cursor()
        c.execute("DELETE FROM sessions WHERE user=? AND token=?", [self.id, token])
        db.conn.commit()

    def authenticate(self, password):
        if not self.exists:
            return False
        c = db.conn.cursor()
        c.execute("SELECT password, salt FROM users WHERE username=? LIMIT 1", [self._username])
        pwd_hash, salt = c.fetchone()
        return pwd_hash == User.hash(password, salt)

    def authenticate_session(self, token):
        c = db.conn.cursor()
        c.execute("SELECT COUNT(*) FROM sessions WHERE user=? AND token=?", self.id, token)
        return c.fetchone()[0] == 1

    def hash(password, salt):
        return hashlib.sha256(str(password+salt).encode()).hexdigest()

    def salt(length=64):
        return "".join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(length))

    def __str__(self):
        return "User({}, id={})".format(self.username, self.id)

    def __repr__(self):
        return str(self)

class Session:

    def __init__(self, user, name, token, created):
        if type(user) is not User:
            raise TypeError
        self.user = user
        self.name = str(name)
        self.token = str(token)
        self.created = int(created)

    def __str__(self):
        return "Session({}..., user={})".format(self.token[:8], self.user)

    def __repr__(self):
        return str(self)
