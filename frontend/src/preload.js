// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    loadUrl: (url) => {
      ipcRenderer.send('load-url', url)
    },
    onUrlChanged: (callback) => ipcRenderer.on('url-changed', (_event, url) => {
        callback(url)
    })
});

window.addEventListener('DOMContentLoaded', () => {
    const urlBar = document.getElementById('url-bar');
    urlBar.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        window.electronAPI.loadUrl(urlBar.value);
      }
    });

    window.electronAPI.onUrlChanged((url) => {
        urlBar.value = url
    })
});