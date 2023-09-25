# Process Governor

**Process Governor** is a Python utility designed to manage Windows processes and services by adjusting their
priorities, I/O priorities, and core affinity based on user-defined rules in a JSON configuration.

[Russian README / Русская версия](README.ru.md)

## Features

- Adjust process and service priorities for better performance.
- Control I/O priorities to optimize resource utilization.
- Define core affinity for processes.
- Fine-tune Windows services and processes based on user-defined rules in the `config.json` file.

## Getting Started

To use Process Governor, follow these steps:

1. Clone this repository.
2. Install the required dependencies using `pip`: `pip install -r requirements.txt`
3. Configure your rules in the `config.json` file. You can create the `config.json` file by running the program once.
4. Run the `process-governor.py` script: `python process-governor.py`

You can close the program by accessing the tray icon.

## Creating a Portable Build

You can create a portable version of the program using **pyvan**. Follow these steps to build the portable version:

1. Run the `python build_portable.py` script.
2. After the script completes, you will find the portable build in the `dist` folder.

Now you have a portable version of the program that you can use without installation.

## Configuration Format

The configuration file for Process Governor is in JSON format. Below, we describe the structure and available parameters
within the `config.json` file.

### JSON Structure for Serialization

To ensure correct deserialization using jsonpickle, make sure the following "py/object" tags are present in the JSON
configuration:

- `"py/object": "configuration.config.Config"`
- `"py/object": "configuration.logs.Logs"`
- `"py/object": "configuration.rule.Rule"`
- `"py/object": "psutil._pswindows.Priority"`
- `"py/object": "psutil._pswindows.IOPriority"`

#### Rule Evaluation

- Process rules are evaluated in the order they appear in the configuration file.
- Service rules take precedence over process rules if a match is found for a service. Once a matching service rule is
  applied, further evaluation of process rules for the same process is ignored.

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
    - Example: `"priority": { "py/object": "psutil._pswindows.Priority", "value": "High" }`

- `ioPriority` (string, optional): Sets the I/O priority for the process or service. Valid values are:
    - `"VeryLow"`
    - `"Low"`
    - `"Normal"`
    - `"High"`
    - Example: `"ioPriority": { "py/object": "psutil._pswindows.IOPriority", "value": "Normal" }`

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
  "py/object": "configuration.config.Config",
  "ruleApplyIntervalSeconds": 1,
  "logging": {
    "py/object": "configuration.logs.Logs",
    "enable": false,
    "filename": "logging.txt",
    "level": "WARN",
    "maxBytes": 1048576,
    "backupCount": 2
  },
  "rules": [
    {
      "py/object": "configuration.rule.Rule",
      "processSelector": "example.exe",
      "priority": {
        "py/object": "psutil._pswindows.Priority",
        "value": "High"
      },
      "ioPriority": {
        "py/object": "psutil._pswindows.IOPriority",
        "value": "Normal"
      },
      "affinity": "1;3-5"
    },
    {
      "py/object": "configuration.rule.Rule",
      "serviceSelector": "Audio*",
      "priority": {
        "py/object": "psutil._pswindows.Priority",
        "value": "Realtime"
      },
      "ioPriority": {
        "py/object": "psutil._pswindows.IOPriority",
        "value": "High"
      },
      "affinity": "0;2;4"
    }
  ]
}
```

In this example, two rules are defined—one for a process and one for a service. Service rules take precedence over
process rules if a match is found for a service.

### License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.