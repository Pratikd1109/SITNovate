document.getElementById("changeColor").addEventListener("click", async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (tab) {
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => { document.body.style.backgroundColor = "lightblue"; }
        });
    }
});
