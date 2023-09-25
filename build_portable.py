import os
import shutil
from pathlib import Path

import pyvan
from genexe.generate_exe import generate_exe
from pyvan import HEADER_NO_CONSOLE

OPTIONS = {
    "main_file_name": "../process-governor.py",
    "show_console": False,
    "use_existing_requirements": True,
    "extra_pip_install_args": [],
    "python_version": None,
    "use_pipreqs": False,
    "install_only_these_modules": [],
    "exclude_modules": [],
    "include_modules": [],
    "path_to_get_pip_and_python_embedded_zip": "downloads_for_van",
    "build_dir": "dist",
    "pydist_sub_dir": "pydist",
    "source_sub_dir": "src",
    "icon_file": "src/resource/favicon.ico",
    "input_dir": "src"
}

original = pyvan.make_startup_exe


def make_startup_exe(main_file_name, show_console, build_dir, relative_pydist_dir, relative_source_dir, icon_file=None):
    """ Make the startup exe file needed to run the script """
    print("Making startup exe file")

    exe_fname = os.path.join(build_dir, os.path.splitext(os.path.basename(main_file_name))[0] + ".exe")
    python_entrypoint = "python.exe"
    command_str = f"{{EXE_DIR}}\\{relative_pydist_dir}\\{python_entrypoint} {{EXE_DIR}}\\{relative_source_dir}\\{main_file_name}"

    generate_exe(
        target=Path(exe_fname),
        command=command_str,
        icon_file=None if icon_file is None else Path(icon_file),
        show_console=show_console
    )

    main_file_name = os.path.join(build_dir, main_file_name)

    if not show_console:
        with open(main_file_name, "r", encoding="utf8", errors="surrogateescape") as f:
            main_content = f.read()
        if HEADER_NO_CONSOLE not in main_content:
            with open(main_file_name, "w", encoding="utf8", errors="surrogateescape") as f:
                f.write(str(HEADER_NO_CONSOLE + main_content))

    shutil.copy(main_file_name, build_dir)

    print("Done!")


pyvan.make_startup_exe = make_startup_exe

pyvan.build(**OPTIONS)
