let server = "http://localhost:80";

chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({color: 'red'}, function() {
        console.log("The color is red");
    });

    database = {};
    defaults = ["example.com", "facebook.com", "youtube.com", "twitter.com", "tumblr.com", "reddit.com", "old.reddit.com", "netflix.com", "messenger.com", "9gag.com","test.com"];
    for (var i=0; i<defaults.length; i++) {
        database[defaults[i]] = {
            ask: true,
            last_asked: 0,
            counter: 0
        }
    }
    chrome.storage.sync.set({db: database})

    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
        chrome.declarativeContent.onPageChanged.addRules([{
            conditions: [new chrome.declarativeContent.PageStateMatcher({
                pageUrl: {schemes: ["http", "https"]}
            })],
            actions: [new chrome.declarativeContent.ShowPageAction()]
        }]);
    });
});
