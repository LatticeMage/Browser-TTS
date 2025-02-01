const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
    loadURL: (url) => {
      ipcRenderer.send('load-url', url);
    },
});