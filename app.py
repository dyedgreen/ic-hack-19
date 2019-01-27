import flask as f
import random

import why


why.db.init()
app = f.Flask(__name__)
app.secret_key = b'en4t432.:ererg%$%&)=sd' # Need to get this somewhere else...


@app.route("/")
def index():
    return f.render_template("index.html")

## WEB APP ROUTES

# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():
    if f.session.get("token"):
        return f.redirect(f.url_for("app_list"))
    username = ""
    error = False
    if f.request.method == "POST":
        username = f.request.form["username"]
        password = f.request.form["password"]
        try:
            f.session["token"] = why.user_api.login("Web Login", username, password)
            f.session.permanent = True
            return f.redirect(f.url_for("app_list"))
        except Exception as e:
            error = str(e)
    return f.render_template("login.html", error=error, username=username)

@app.route("/login/<string:token>", methods=["POST", "GET"])
def login_token(token):
    if f.session.get("token"):
        return "", 204
    try:
        why.user_api.is_logged_in(token)
        f.session["token"] = token
        f.session.permanent = True
    except Exception as e:
        return str(e), 400
    return "", 204

@app.route("/logout/<string:token>", methods=["GET", "POST"])
def logut(token):
    why.user_api.logout(token)
    return f.redirect(f.url_for("login"))

@app.route("/sessions", methods=["GET"])
def session_list():
    if not f.session.get("token"):
        return f.redirect(f.url_for("login"))
    try:
        session_list = why.user.User.from_session(f.session["token"]).sessions
    except:
        return f.redirect(f.url_for("login"))
    return f.render_template("session_list.html", list=session_list)

@app.route("/apps", methods=["GET"])
def app_list():
    if not f.session.get("token"):
        return f.redirect(f.url_for("login"))
    try:
        app_list = why.reason.App.get_for_user(why.user.User.from_session(f.session["token"]))
    except:
        f.session["token"] = False
        return f.redirect(f.url_for("login"))
    return f.render_template("app_list.html", list=app_list, token=f.session["token"])

@app.route("/app/<string:uri>", methods=["GET"])
def reason_list(uri):
    if not f.session.get("token"):
        return f.redirect(f.url_for("login"))
    try:
        app = why.reason.App(uri, why.user.User.from_session(f.session["token"]))
        if not app.exists:
            raise Exception
    except:
        f.abort(404)
    return f.render_template("reason_list.html", app=app, list=app.reasons)


## API ROUTES

# USER ROUTES

@app.route("/api/user/register", methods=["POST"])
def api_user_register():
    username = f.request.values["username"]
    password = f.request.values["password"]
    try:
        why.user_api.create(username, password)
    except Exception as e:
        return f.jsonify({"error":str(e)}), 400
    return f.jsonify({"error":False})

@app.route("/api/user/<string:username>/update", methods=["POST", "PUT"])
def api_user_update(username):
    old_pwd = f.request.values["old_password"]
    new_pwd = f.request.values["new_password"]
    try:
        why.user_api.update_password(username, old_pwd, new_pwd)
    except Exception as e:
        return f.jsonify({"error":str(e)}), 400
    return f.jsonify({"error":False})

@app.route("/api/user/login/<string:app_name>", methods=["POST"])
def api_user_login(app_name):
    username = f.request.values["username"]
    password = f.request.values["password"]
    result = {"error":False, "token":""}
    try:
        result["token"] = why.user_api.login(app_name, username, password)
    except Exception as e:
        result["error"] = str(e)
        return f.jsonify(result), 400
    return f.jsonify(result)

@app.route("/api/user/login/exists", methods=["GET"])
def api_user_login_exists():
    token = f.request.values["token"]
    res = {"error":False, "exists":True}
    try:
        why.user_api.is_logged_in(token)
    except Exception as e:
        res["error"] = str(e)
        res["exists"] = False
    return f.jsonify(res)

@app.route("/api/user/logout/<string:token>", methods=["POST", "DELETE"])
def api_user_logout(token):
    why.user_api.logout(token)
    return "", 204

# APP (REASONS) ROUTES

@app.route("/api/app/<string:uri>", methods=["GET"])
def api_app_get(uri):
    token = f.request.values["token"]
    res = {
        "error": False,
        "uri": "",
        "name": "",
        "icon": "",
    }
    try:
        app = why.reason_api.get(token, uri)
        res["uri"] = uri
        res["name"] = app.name
        res["icon"] = app.icon
    except Exception as e:
        res["error"] = str(e)
        return f.jsonify(res), 400
    return f.jsonify(res)

@app.route("/api/app/<string:uri>/create", methods=["POST"])
def api_app_create(uri):
    token = f.request.values["token"]
    name = f.request.values["name"]
    icon = f.request.values["icon"]
    res = {"error":False}
    try:
        why.reason_api.create(token, uri, name, icon)
    except Exception as e:
        res["error"] = str(e)
        return f.jsonify(res), 400
    return f.jsonify(res)

@app.route("/api/app/<string:uri>/reasons", methods=["GET"])
def api_app_reasons(uri):
    token = f.request.values["token"]
    res = {"error":False, "reasons": []}
    try:
        res["reasons"] = why.reason_api.list(token, uri)
    except Exception as e:
        res["error"] = str(e)
        return f.jsonify(res), 400
    return f.jsonify(res)

@app.route("/api/app/<string:uri>/reasons/add", methods=["POST"])
def api_app_reasons_add(uri):
    token = f.request.values["token"]
    reason = f.request.values["reason"]
    res = {"error":False}
    try:
        why.reason_api.add_reason(token, uri, reason)
    except Exception as e:
        res["error"] = str(e)
        return f.jsonify(res), 400
    return f.jsonify(res)
