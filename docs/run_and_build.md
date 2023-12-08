# Running from source and creating a portable build

[![README](icons/readme.png) README](README.md) | [![RU](icons/ru.png) Русская версия](run_and_build.ru.md)

---

## Running from source code

To run **Process Governor** from source code, follow these steps:

1. Clone this repository.
2. Install the required dependencies using `pip`: `pip install -r requirements.txt`
3. Run the `process-governor.py` script with **administrative privileges**: `python process-governor.py`
4. [Configure the rules](docs/ui_rule_configurator.md) for processes and services.

## Creating a portable build

You can create a portable version of the program using **PyInstaller**. Follow these steps to build the portable
version:

1. Install PyInstaller using `pip install pyinstaller`.
2. Run the `python build_portable.py` script.
3. After the script completes, you will find the portable build in the `dist` folder.

Now you have a portable version of the program that you can use without installation.
