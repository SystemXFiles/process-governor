![Logo Process Governor](docs/images/github-banner-readme.png)

[![RU](docs/icons/ru.png) Русская версия](docs/README.ru.md)

---

**Process Governor** is a Python utility designed to manage Windows processes and services by adjusting their
priorities, I/O priorities, and core affinity based on user-defined rules in a JSON configuration.

## Features

- Adjust process and service priorities for better performance.
- Control I/O priorities to optimize resource utilization.
- Define core affinity for processes.
- Fine-tune Windows services and processes based on [user-defined rules](#configuration-format) in the `config.json`
  file.
- Continuous monitoring of the configuration file for rule application.
- The ability to add a program to autostart.

## Getting Started

To get started with **Process Governor**, follow these steps:

1. Download the latest ready-to-use build from the following
   link: [Latest Release](https://github.com/SystemXFiles/process-governor/releases/latest).
2. [Configure your rules](#configuration-format) in the `config.json` file. You can create the `config.json` file by
   running the program once.
3. Run the `Process Governor.exe` executable with **administrative privileges**.
   This is important to allow the program to make the necessary adjustments to process and service priorities, I/O
   priorities, and core affinity.

You can close the program by accessing the tray icon:

![Tray menu screenshot](docs/images/tray_menu_screenshot.png)

## Tips and Tricks

1. [Optimizing Audio on PC](docs/tips'n'tricks/audio.md)
2. [Starfield Optimization: Reduce Stutters](docs/tips'n'tricks/starfield.md)

---

## Running from source code

To run **Process Governor** from source code, follow these steps:

1. Clone this repository.
2. Install the required dependencies using `pip`: `pip install -r requirements.txt`
3. [Configure your rules](#configuration-format) in the `config.json` file. You can create the `config.json` file by
   running the program once.
4. Run the `process-governor.py` script with **administrative privileges**: `python process-governor.py`

## Creating a Portable Build

You can create a portable version of the program using **PyInstaller**. Follow these steps to build the portable
version:

1. Install PyInstaller using `pip install pyinstaller`.
2. Run the `python build_portable.py` script.
3. After the script completes, you will find the portable build in the `dist` folder.

Now you have a portable version of the program that you can use without installation.

---

## Configuration Format

The configuration file for Process Governor is in JSON format and is named `config.json`. If the configuration file is
missing, run the program once, and it will be created automatically.

Additionally, it's important to note that Process Governor continuously monitors and applies the rules from the
configuration file at regular intervals to ensure proper process and service management. This automated process allows
for dynamic optimization based on the specified rules.

Below, we provide an overview of the file's structure and the available parameters.

### `rules` Section

The `rules` section defines how Process Governor will manage processes and services. Each rule is represented as a JSON
object within an array.

- `processSelector` (string, optional): Specifies the process name or pattern to match. You can use wildcards,
  including `*` and `?`, to match multiple processes. Process rules are evaluated in the order they appear in the
  configuration
  file.
    - Example: `"processSelector": "example.exe"`
    - Example with wildcards: `"processSelector": "logioptionsplus_*.exe"`

- `serviceSelector` (string, optional): Specifies the service name or pattern to match. You can use wildcards,
  including `*` and `?`, to match multiple services. Service rules have a higher priority than process rules and will
  override them if a match is found.
    - Example: `"serviceSelector": "MyService"`
    - Example with wildcards: `"serviceSelector": "Audio*"`

- `priority` (string, optional): Sets the process or service priority. Valid values are:
    - `"Idle"`
    - `"BelowNormal"`
    - `"Normal"`
    - `"AboveNormal"`
    - `"High"`
    - `"Realtime"`
    - Example: `"priority": "High"`

- `ioPriority` (string, optional): Sets the I/O priority for the process or service. Valid values are:
    - `"VeryLow"`
    - `"Low"`
    - `"Normal"`
    - `"High"`: Setting the I/O priority to "High" may result in an AccessDenied error in most cases.
    - Example: `"ioPriority": "Normal"`

- `affinity` (string, optional): Specifies CPU core affinity. You can define affinity as:
    - A range, inclusive (e.g., "1-5").
    - Specific cores (e.g., "1;2;3;4;5").
    - A combination of both (e.g., "1-4;5").
    - Example (range): `"affinity": "1-4"`
    - Example (specific cores): `"affinity": "0;2;4"`
    - Example (combination): `"affinity": "1;3-5"`

### Example Configuration

Here's an example `config.json` file with rules:

```json
{
  "ruleApplyIntervalSeconds": 1,
  "logging": {
    "enable": true,
    "filename": "logging.txt",
    "level": "WARN",
    "maxBytes": 1048576,
    "backupCount": 2
  },
  "rules": [
    {
      "processSelector": "example.exe",
      "priority": "High",
      "ioPriority": "Normal",
      "affinity": "1;3-5"
    },
    {
      "serviceSelector": "Audio*",
      "priority": "Realtime",
      "ioPriority": "High",
      "affinity": "0;2;4"
    }
  ]
}
```

In this example, two rules are defined—one for a process and one for a service.

---

### License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.