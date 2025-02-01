const { app, BrowserWindow, ipcMain, Menu, globalShortcut } = require('electron');
const path = require('path');

let win; // Make win accessible outside createWindow

function createWindow() {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: false, // Disable nodeIntegration for security
            contextIsolation: true, // Enable context isolation for security
            webviewTag: true // Enable <webview> tag support
        }
    });

    // Load the HTML file which contains the address bar
    win.loadFile(path.join(__dirname, 'index.html'));

     // Register F12 shortcut
     globalShortcut.register('F12', () => {
       win.toggleDevTools();
     });


    // Menu
    const mainMenuTemplate = [
         {
            label: 'Edit',
            submenu: [
              {
                label: 'Quit',
                accelerator: process.platform == 'darwin' ? 'Command+Q' : 'Ctrl+Q',
                click() {
                  app.quit();
                }
              }
            ],
          },
        {
          label: 'Dev Tools',
          submenu: [
            {
              label: 'Reload Page',
              accelerator: 'CommandOrControl+R',
              click(){
                win.reload();
              }
            },
             {
              label: 'Show Dev Tools',
              accelerator: process.platform == 'darwin' ? 'Command+I' : 'Ctrl+I',
              click(){
                win.toggleDevTools();
              }
            },

          ]
        }
      ];
      const mainMenu = Menu.buildFromTemplate(mainMenuTemplate);
      Menu.setApplicationMenu(mainMenu);
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