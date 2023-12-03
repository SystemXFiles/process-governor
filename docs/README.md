![Logo Process Governor](images/github-banner-readme.png)

[![RU](icons/ru.png) Русская версия](README.ru.md)

---

**Process Governor** is a Python utility designed to manage Windows processes and services by adjusting their
priorities, I/O priorities, and core affinity based on user-defined rules in a JSON configuration.

## Features

- Adjust process and service priorities for better performance.
- Control I/O priorities to optimize resource utilization.
- Define core affinity for processes.
- Fine-tune Windows services and processes based on [user-defined rules](ui_rule_configurator.md).
- Continuous monitoring of the configuration file for rule application.
- Ability to add ProcessGovernor to autorun.

## Getting started

To get started with **Process Governor**, follow these steps:

1. Download the latest ready-to-use build from the following
   link: [Latest Release](https://github.com/SystemXFiles/process-governor/releases/latest).
2. Run the `Process Governor.exe` executable with **administrative privileges**.
   This is important to allow the program to make the necessary adjustments to process and service priorities, I/O
   priorities, and core affinity.
3. [Configure the rules](ui_rule_configurator.md) for processes and services.

You can close the program by accessing the tray icon.

## Knowledge base

* [Configuring rules](ui_rule_configurator.md)
* [Configuration file](configuration_file.md)
* [Optimizing Audio on PC](tips'n'tricks/audio.md)
* [Starfield Optimization: Reduce Stutters](tips'n'tricks/starfield.md)

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

---

### License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.