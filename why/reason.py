"""
Handles apps and reasons
"""

from . import db


class App:

    def __init__(self, uri, user):
        self.uri = uri
        self.user = user
        self.id = None
        self.name = ""
        self.icon = ""

        c = db.conn.cursor()
        c.execute(
            "SELECT id, name, icon FROM apps WHERE uri=? AND user=? LIMIT 1",
            [self.uri, self.user.id])
        res = c.fetchone()
        if res is not None:
            self.id = res[0]
            self.name = res[1]
            self.icon = res[2]

    def create(uri, user, name, icon):
        if not user.exists:
            raise ValueError("User does not exists")
        if len(uri) == 0 or len(name) == 0:
            raise ValueError("Missing values")
        # Check if user already has this app
        c = db.conn.cursor()
        c.execute("SELECT COUNT(*) FROM apps WHERE uri=? AND user=?", [uri, user.id])
        if c.fetchone()[0] > 0:
            raise ValueError("App already exists")
        c.execute(
            "INSERT INTO apps (uri, user, name, icon) VALUES (?,?,?,?)",
            [str(uri), user.id, str(name), str(icon)])
        db.conn.commit()
        return App(uri, user)

    def get_for_user(user):
        if not user.exists:
            raise ValueError("User does not exists")
        c = db.conn.cursor()
        # Could be optimized
        c.execute("SELECT uri FROM apps WHERE user=?", [user.id])
        apps = []
        for row in c:
            apps.append(App(row[0], user))
        return apps

    @property
    def exists(self):
        return self.id is not None

    @property
    def reasons(self):
        c = db.conn.cursor()
        c.execute("SELECT reason FROM reasons WHERE app=?", [self.id])
        res = []
        for row in c:
            res.append(row[0])
        return res

    def add_reason(self, reason):
        if len(reason) == 0:
            raise ValueError("Need a reason")
        c = db.conn.cursor()
        c.execute("INSERT INTO reasons (app, reason) VALUES (?, ?)", [self.id, str(reason)])
        db.conn.commit()

    def __str__(self):
        return "App({}, id={}, uri={}, icon={}, user={})".format(
            self.name, self.id, self.uri, self.icon, self.user)
