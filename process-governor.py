import sys, os
if sys.executable.endswith('pythonw.exe'):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.path.join(os.getenv('TEMP'), 'stderr-{}'.format(os.path.basename(sys.argv[0]))), "w")
    
import platform
import pyuac
from util import pyuac_fix
from util.lock_instance import create_lock_file, remove_lock_file

from main_loop import start_app

if __name__ == "__main__":
    if not platform.system() == "Windows":
        print("Process Governor is intended to run on Windows only.")
        sys.exit(1)

    if not pyuac.isUserAdmin():
        pyuac_fix.runAsAdmin(wait=False, showCmd=False)
    else:
        create_lock_file()
        try:
            start_app()
        finally:
            remove_lock_file()
