import glob
import os
import shutil

import PyInstaller.__main__
import pyinstaller_versionfile

from constants.any import CONFIG_FILE_NAME
from constants.app_info import APP_NAME, APP_VERSION, APP_AUTHOR, APP_NAME_WITH_VERSION

# Setting paths and configuration parameters
VERSION_FILE = "versionfile.txt"
DIST = os.path.join(os.getcwd(), 'dist')
APP_DIST = os.path.join(DIST, APP_NAME)
APP_DIST_WITH_VERSION = os.path.join(DIST, APP_NAME_WITH_VERSION)
CONFIG_FILE_FOR_TESTS = os.path.join(os.getcwd(), CONFIG_FILE_NAME)
CONFIG_FILE_IN_APP_DIST = os.path.join(APP_DIST, CONFIG_FILE_NAME)
SPEC_FILES = r".\*.spec"

# Deleting existing .spec files to clean up the directory
for filename in glob.glob(SPEC_FILES):
    os.remove(filename)

# Creating a version file for the executable
pyinstaller_versionfile.create_versionfile(
    output_file=VERSION_FILE,
    version=APP_VERSION,
    company_name=APP_AUTHOR,
    file_description=APP_NAME,
    internal_name=APP_NAME,
    legal_copyright=f"© {APP_AUTHOR}",
    original_filename=f"{APP_NAME}.exe",
    product_name=APP_NAME
)

# Running PyInstaller to build the application
PyInstaller.__main__.run([
    'process-governor.py',                      # Source script file
    '--clean',                                  # Clean previous builds
    '--noconfirm',                              # No confirmation when deleting dist directory
    '--onedir',                                 # Build the app in one directory
    '--uac-admin',                              # Request admin rights on launch
    '--hide-console', 'hide-early',             # Hide the console on startup
    '--add-data', './resources/*;./resources',  # Add additional resources
    '--contents-directory', 'scripts',          # Directory for Python and app scripts in the built package
    '--icon', 'resources/app.ico',              # Application icon
    '--debug', 'noarchive',                     # Disables bundling of application scripts inside the exe
    '--name', APP_NAME,                         # Name of the executable file
    '--version-file', VERSION_FILE,             # Path to the version file
    '--distpath', DIST,                         # Directory to save the built application
])

# Creating an archive of the built application
shutil.make_archive(APP_DIST_WITH_VERSION, 'zip', APP_DIST)

# Copying the configuration file for tests into the built application
if os.path.isfile(CONFIG_FILE_FOR_TESTS):
    shutil.copyfile(CONFIG_FILE_FOR_TESTS, CONFIG_FILE_IN_APP_DIST)
