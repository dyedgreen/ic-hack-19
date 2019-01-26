import flask as f

import why


why.db.init()
app = f.Flask(__name__)

@app.route("/")
def test():
    return f.render_template("index.html")

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
