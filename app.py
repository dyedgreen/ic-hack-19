import flask as f

import why


why.db.init()
app = f.Flask(__name__)

@app.route("/")
def test():
    return f.render_template("index.html")

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
