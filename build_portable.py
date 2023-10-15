import PyInstaller.__main__

PyInstaller.__main__.run([
    'process-governor.py',
    '--noconfirm',
    '--onedir',
    '--uac-admin',
    '--hide-console', 'hide-early',
    '--add-data', './resources/*;./resources',
    '--contents-directory', 'scripts',
    '--icon', 'resources/app.ico',
    '--name', 'Process Governor',
    '--debug', 'noarchive',
])