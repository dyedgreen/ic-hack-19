let checkbox = document.getElementById("ask-checkbox");
let stats = document.getElementById("stats")
let span = document.getElementById("hostname")
let logo = document.getElementById("logo")
logo.src = chrome.runtime.getURL("images/brand.png");
let server = "http://localhost:80";
let host = "";
let favicon = "";

function switcher() {
    chrome.storage.sync.get(['db','token'], function(data) {
        db = data.db;
        if (typeof data.db[host] === "undefined") {
            db[host] = {
                ask: checkbox.checked,
                last_asked: 0,
                counter: 0
            }
            var xhttp = new XMLHttpRequest();
            xhttp.open("POST", server+"/api/app/"+host+"/create", true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("token="+data.token+"&name="+host+"&icon="+favicon);
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4) {
                    console.log(this);
                }
            }
        } else {
            db[host]["ask"] = checkbox.checked;
        }
        chrome.storage.sync.set({db: db});
    });
    checkbox.checked;
    // location.reload();
}

chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    url = tabs[0].url;
    favicon = tabs[0].favIconUrl;
    var parser = document.createElement('a');
    parser.href = url;
    host = parser.hostname;
    host = host.slice(0,4) == "www." ? host.slice(4) : host;
    span.innerHTML = host;

    checkbox.onclick = switcher;

    chrome.storage.sync.get('db', function(data) {
        if (typeof data.db[host] !== "undefined") {
            checkbox.checked = data.db[host]["ask"];
            if (data.db[host]["ask"]) {
                access_info = document.createElement("p");
                access_info.innerHTML = "You have tried accessing this website <b>"+data.db[host]["counter"]+"</b> times today."
                stats.appendChild(access_info)
            } else {
                access_info = document.createElement("p");
                access_info.innerHTML = "No data available on this website for today."
                stats.appendChild(access_info)
            }
        } else {
            access_info = document.createElement("p");
            access_info.innerHTML = "No data available on this website for today."
            stats.appendChild(access_info)
        }
        link = document.createElement("a");
        link.innerHTML = "Show full history online!"
        stats.appendChild(link)
    })
});
