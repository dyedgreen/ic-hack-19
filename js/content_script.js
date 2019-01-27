let body = document.body;
let br = document.createElement("br");

class MessageBox {
    constructor(type, text) {
        this.div = document.createElement("div");
        this.div.classList.add("why--message-"+type);
        this.div.innerHTML = text;
    }
}

function saveResponse() {
    r_input.blur()
    reply.classList.remove("why--reply-box")
    send.classList.add("why--sent")
    message1 = new MessageBox("from", "Ok, thanks!");
    message1.div.style.animationName = "fade-in"
    message1.div.style.animationDuration = "0.5s"
    chat_window.appendChild(message1.div);
    setTimeout(function() {
        document.getElementById("why--container").classList.add("why--fadeout");
        setTimeout(function() {
            document.getElementById("why--container").style.display = "none";
        }, 500)
    }, 1000);
}

let container = document.createElement("div");
container.id = "why--container";

let chat_window = document.createElement("div");
chat_window.id = "why--chat-window";
container.appendChild(chat_window);

message1 = new MessageBox("from", "Why?");
chat_window.appendChild(message1.div);

chat_window.appendChild(br);

reply = document.createElement("div");
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
chat_window.appendChild(send)

body.appendChild(container);
document.getElementById("why--reply-textarea").focus();
