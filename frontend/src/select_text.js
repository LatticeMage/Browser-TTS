// select_text.js

function handleSelectionChange() {
    const selectedText = window.getSelection().toString();
    const selectedTextDisplay = document.getElementById('selected-text');

    if (selectedTextDisplay) {
        selectedTextDisplay.textContent = selectedText;
    }
}


// This is a simple way to check if we are in the main app, not in webview
if (window.location.protocol === 'file:') {
    document.addEventListener('selectionchange', handleSelectionChange);
} else {
  // for webview
  window.api = {
    handleSelectionChange: handleSelectionChange
  };
}