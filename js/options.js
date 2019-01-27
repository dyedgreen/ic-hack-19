let body = document.body;
let container = document.getElementById("container");
let server = "http://localhost:80"
let toast_cotainer = document.getElementById("toasts")

function toast(format, text) {
    let div = document.createElement("div");
    div.classList.add("toast");
    div.classList.add(format);
    div.innerText = text;
    toast_cotainer.appendChild(div);
    setTimeout(function() {
        div.classList.add("expired");
    }, 5000)
}

function register_request() {
    u = document.getElementById("username").value;
    p = document.getElementById("password").value;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", server+"/api/user/register", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("username="+u+"&password="+p);
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            let res = JSON.parse(this.responseText);
            console.log(res)
            if (typeof res !== "object") {
                toast("error", "Corrupted response data.");
            } else if (res["error"] !== false) {
                toast("error", res["error"]);
            } else {
                toast("success", "User account created!");
                login_request();
            }
        }
    }
}

function login_request() {
    u = document.getElementById("username").value;
    p = document.getElementById("password").value;
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", server+"/api/user/login/chrome-extension", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("username="+u+"&password="+p);
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            let res = JSON.parse(this.responseText);
            console.log(res)
            if (typeof res !== "object") {
                toast("error", "Corrupted response data.");
            } else if (res["error"] !== false) {
                toast("error", res["error"]);
            } else {
                chrome.storage.sync.set({'token': res["token"], 'username': u}, function() {
                    toast("success", "Logged in successfully!");
                    build_view();
                });
            }
        }
    }
}

function login_keydown(e) {
    if (e.keyCode === 13) {
        e.preventDefault();
        login_request();
    }
}

function logout_request() {
    chrome.storage.sync.get('token', function(data) {
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", server+"/api/user/logout/"+data.token, true);
        xhttp.send();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                chrome.storage.sync.remove('token', function() {
                    toast("success", "Logged out!");
                    build_view();
                })
            }
        }
    });
}

function change_password_request() {
    chrome.storage.sync.get(['username'], function(data) {
        o = document.getElementById("old_password").value;
        n = document.getElementById("new_password").value;
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", server+"/api/user/"+data.username+"/update", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("old_password="+o+"&new_password="+n);
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                let res = JSON.parse(this.responseText);
                console.log(res)
                if (typeof res !== "object") {
                    toast("error", "Corrupted response data.");
                } else if (res["error"] !== false) {
                    toast("error", res["error"]);
                } else {
                    toast("success", "Changed password successfully!");
                }
            }
        }
    });
}

function change_password_keydown(e) {
    if (e.keyCode === 13) {
        e.preventDefault();
        change_password_request();
    }
}

logo = document.createElement("img")
logo.src = chrome.runtime.getURL("images/brand.png")
logo.id = "logo"

function build_view() {
    container.innerHTML = ""
    chrome.storage.sync.get(['token', 'username'], function(data) {
        console.log(data)
        if (typeof data.token === "undefined") {
            container.appendChild(logo)

            login_message = document.createElement("p");
            login_message.innerHTML = "Login to <b>Why?</b> to store your answers and history!";
            container.appendChild(login_message);

            username = document.createElement("input");
            username.type = "text";
            username.id = "username";
            username.placeholder = "username";
            username.addEventListener('keydown', login_keydown);
            container.appendChild(username);

            password = document.createElement("input");
            password.type = "password";
            password.id = "password";
            password.placeholder = "password";
            password.addEventListener('keydown', login_keydown);
            container.appendChild(password);

            login = document.createElement("button");
            login.id = "login_button";
            login.innerHTML = "Login";
            login.onclick = login_request;
            login.classList.add("half-button");
            container.appendChild(login);

            register = document.createElement("button");
            register.id = "register_button";
            register.innerHTML = "Register";
            register.onclick = register_request;
            register.classList.add("half-button");
            container.appendChild(register);
        } else {
            container.appendChild(logo)

            greeting = document.createElement("p");
            greeting.innerHTML = "Logged into <b>Why?</b> as "+data.username;
            container.appendChild(greeting);

            logout = document.createElement("button");
            logout.id = "logout_button";
            logout.innerHTML = "Logout";
            logout.onclick = logout_request;
            container.appendChild(logout);

            old_password = document.createElement("input");
            old_password.type = "password";
            old_password.id = "old_password";
            old_password.placeholder = "old password";
            old_password.style.marginTop = "50px";
            old_password.addEventListener('keydown', change_password_keydown);
            container.appendChild(old_password);

            new_password = document.createElement("input");
            new_password.type = "password";
            new_password.id = "new_password";
            new_password.placeholder = "new password";
            new_password.addEventListener('keydown', change_password_keydown);
            container.appendChild(new_password);

            change_password = document.createElement("button");
            change_password.id = "change_password_button";
            change_password.innerHTML = "Change password";
            change_password.onclick = change_password_request;
            container.appendChild(change_password);
        }
    });
}
build_view();
