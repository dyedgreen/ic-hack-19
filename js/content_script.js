let body = document.body;
let br = document.createElement("br");

class MessageBox {
    constructor(type, text) {
        this.div = document.createElement("div");
        this.div.classList.add("why--message-"+type);
        this.div.innerHTML = text;
    }
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
reply.innerHTML = "Because I'm bored";
chat_window.appendChild(reply);

send = document.createElement("img");
send.id = "why--send"
send.src = chrome.runtime.getURL("images/send.svg")
chat_window.appendChild(send)

body.appendChild(container);
