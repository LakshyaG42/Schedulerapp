// background.js
// Author:
// Author URI: https://
// Author Github URI: https://www.github.com/
// Project Repository URI: https://github.com/
// Description: Handles all the browser level activities (e.g. tab management, etc.)
// License: MIT
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'add_event') {
        // Store the event data in an array or send it to your Python script.
        const event = message.event;
        // Send data to Python using an external messaging method
        // Example: chrome.runtime.connectNative('your_native_app');
    }
});