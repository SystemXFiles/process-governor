import os
import sys
from logging import getLogger
from subprocess import list2cmdline

log = getLogger('pyuac')


def runAsAdmin(cmdLine=None, wait=True, showCmd=True):
    if os.name != 'nt':
        raise RuntimeError("This function is only implemented on Windows.")

    import win32con
    import win32event
    import win32process
    # noinspection PyUnresolvedReferences
    from win32com.shell.shell import ShellExecuteEx
    # noinspection PyUnresolvedReferences
    from win32com.shell import shellcon

    if not cmdLine:
        cmdLine = [sys.executable] + sys.argv
        if not os.path.exists(sys.argv[0]):
            # When running an entry point, argv[0] is wrong
            for ext in ('-script.py', '-script.pyw'):
                if os.path.exists(sys.argv[0] + ext):
                    cmdLine[1] = sys.argv[0] + ext
                    break
        log.debug("Defaulting to runAsAdmin command line: %r", cmdLine)
    elif type(cmdLine) not in (tuple, list):
        raise ValueError("cmdLine is not a sequence.")

    if showCmd:
        showCmdArg = win32con.SW_SHOWNORMAL
    else:
        showCmdArg = win32con.SW_HIDE

    lpVerb = 'runas'  # causes UAC elevation prompt.

    cmd = cmdLine[0]
    params = list2cmdline(cmdLine[1:])

    log.info("Running command %r - %r", cmd, params)
    procInfo = ShellExecuteEx(
        nShow=showCmdArg,
        fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
        lpVerb=lpVerb,
        lpFile=cmd,
        lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        _ = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        log.info("Process handle %s returned code %s", procHandle, rc)
    else:
        rc = None

    return rc
