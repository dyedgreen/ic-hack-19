let server = "http://localhost:80";

chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({color: 'red'}, function() {
        console.log("The color is red");
    });

    database = {};
    defaults = ["example.org", "facebook.com", "youtube.com", "twitter.com", "tumblr.com", "reddit.com", "old.reddit.com", "netflix.com", "messenger.com", "9gag.com","test.com"];
    favicons = ["", "https://www.facebook.com/favicon.ico", "https://www.youtube.com/favicon.ico", "https://twitter.com/favicon.ico", "https://assets.tumblr.com/images/favicons/favicon.ico", "https://www.reddit.com/favicon.ico", "https://old.reddit.com/favicon.ico", "https://www.netflix.com/favicon.ico", "https://static.xx.fbcdn.net/rsrc.php/y7/r/O6n_HQxozp9.ico", "https://9gag.com/favicon.ico", "https://www.test.com/favicon.ico"]
    for (var i=0; i<defaults.length; i++) {
        database[defaults[i]] = {
            ask: true,
            last_asked: 0,
            counter: 0,
            favicon: encodeURIComponent(favicons[i]),
            reasons: []
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

    chrome.runtime.openOptionsPage();
});
