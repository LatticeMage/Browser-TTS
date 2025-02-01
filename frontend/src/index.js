// index.js

const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

let win; // Make win accessible to `updateUrlInput`
function createWindow() {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false, // important to prevent preload script from accessing node
            contextIsolation: true, // important for security
        }
    });
    win.loadFile(path.join(__dirname, 'index.html'));
    
    win.webContents.on('did-navigate', (event, url) => {
        win.webContents.send('url-changed', url);
    });

    win.webContents.on('did-finish-load', () => {
        win.webContents.send('url-changed', win.webContents.getURL());
    });
}



app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});


ipcMain.on('load-url', (event, url) => {
   win.loadURL(url);
});