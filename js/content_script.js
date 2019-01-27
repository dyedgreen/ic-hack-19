let body = document.body;
let br = document.createElement("br");
let server = "http://localhost:80";
let host = "";

class MessageBox {
    constructor(type, text) {
        this.div = document.createElement("div");
        this.div.classList.add("why--message-"+type);
        this.div.innerHTML = text;
    }
}

function saveResponse() {
    reply = document.getElementById("why--reply-bubble")
    r_input = document.getElementById("why--reply-textarea")
    send = document.getElementById("why--send")
    chat_window = document.getElementById("why--chat-window")
    container = document.getElementById("why--container")

    r_input.blur()
    reply.classList.remove("why--reply-box")
    send.classList.add("why--sent")
    message1 = new MessageBox("from", "Ok, thanks!");
    message1.div.style.animationName = "fade-in"
    message1.div.style.animationDuration = "0.5s"
    chat_window.appendChild(message1.div);

    chrome.storage.sync.get(["db", "token"], function(data) {
        db = data.db;
        db[host]["last_asked"] = new Date().getTime() / 1000 / 60;
        chrome.storage.sync.set({db: db});
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", server+"/api/app/"+host+"/reasons/add", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send("token="+data.token+"&reason="+r_input.value);
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                console.log(this);
            }
        }
    });

    setTimeout(function() {
        container.classList.add("why--fadeout");
        setTimeout(function() {
            container.style.display = "none";
        }, 500)
    }, 1000);
}

function ask() {
    let container = document.createElement("div");
    container.id = "why--container";

    let chat_window = document.createElement("div");
    chat_window.id = "why--chat-window";
    container.appendChild(chat_window);

    message1 = new MessageBox("from", "Why?");
    chat_window.appendChild(message1.div);

    chat_window.appendChild(br);

    reply = document.createElement("div");
    reply.id = "why--reply-bubble"
    reply.classList.add("why--message-to");
    reply.classList.add("why--reply-box");

    r_input = document.createElement("input");
    r_input.type = "text"
    r_input.id = "why--reply-textarea";
    r_input.placeholder = "Because...";
    r_input.addEventListener('keydown', function (e) {
        if (e.keyCode === 13) {
            e.preventDefault();
            saveResponse();
        }
    });
    reply.appendChild(r_input);

    chat_window.appendChild(reply);

    send = document.createElement("img");
    send.id = "why--send";
    send.src = chrome.runtime.getURL("images/send.svg")
    send.addEventListener('click', function(e) {
        saveResponse();
    })
    chat_window.appendChild(send);

    body.appendChild(container);
    document.getElementById("why--reply-textarea").focus();
}

host = window.location.host;
host = host.slice(0,4) == "www." ? host.slice(4) : host;

chrome.storage.sync.get("db", function(data) {
    db = data.db;
    if (typeof db[host] !== "undefined") {
        current = new Date().getTime() / 1000 / 60;
        diff = current - db[host]["last_asked"];
        if (db[host]["ask"] && diff > 1) {
            if (Math.floor(db[host]["last_asked"]/1440) !== Math.floor(current/1440)) {
                db[host]["counter"] = 1;
            } else {
                db[host]["counter"] += 1;
            }
            db[host]["last_asked"] = current;
            chrome.storage.sync.set({db: db}, function() {
                ask();
            })
        }
    }
})
