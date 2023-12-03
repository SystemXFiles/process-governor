# Process Governor Configuration File

[![README](icons/readme.png) README](../README.md) | [![EN](icons/gb.png) Русская версия](configuration_file.ru.md)

---

The `config.json` configuration file is used to manage the behavior of the **Process Governor** application. It allows
you to define how the application will regulate the priorities of processes and services, their I/O priorities, and
correspondence to CPU cores.

The configuration file is regularly checked by the application and applied if there are changes.

### Configuration File Example

In this example, two rules are defined: one for a process and one for a service.

```json
{
  "ruleApplyIntervalSeconds": 1,
  "logging": {
    "enable": true,
    "level": "WARN",
    "maxBytes": 1024,
    "backupCount": 1
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
    // Additional rules...
  ]
}
```

## Structure of the `config.json`

The configuration file consists of several key sections:

### `ruleApplyIntervalSeconds`

This parameter defines the interval in seconds at which rules will be applied to processes and services. The default
value is `1`, which means that rules are applied every second.

### `logging`

This section contains logging settings. It allows you to enable or disable logging, set the logging level, the maximum
size of the log file, and the number of backup log files to keep.

#### Possible parameters:

- `enable`: Enables or disables logging.
- `level`: The logging level (`INFO`, `WARN`, etc.).
- `maxBytes`: The maximum size of the log file in bytes.
- `backupCount`: The number of backup log files.

### `rules`

This section defines the list of rules by which **Process Governor** will manage processes and services. Each rule is
defined by an object with a set of parameters.

#### Possible parameters:

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

- `priority` (string, optional): Sets the process or service priority.
  Valid values are:
    - `"Idle"`
    - `"BelowNormal"`
    - `"Normal"`
    - `"AboveNormal"`
    - `"High"`
    - `"Realtime"`
    - Example: `"priority": "High"`

- `ioPriority` (string, optional): Sets the I/O priority for the process or service.
  Valid values are:
    - `"VeryLow"`
    - `"Low"`
    - `"Normal"`
    - `"High"`: Setting the I/O priority to "High" may result in an AccessDenied error in most cases.
    - Example: `"ioPriority": "Normal"`

- `affinity` (string, optional): Specifies CPU core affinity.
  You can define affinity as:
    - Range (inclusive): `"affinity": "1-4"`
    - Specific cores: `"affinity": "0;2;4"`
    - Combination: `"affinity": "1;3-5"`

### Validation

Built-in validation prevents the simultaneous assignment of `processSelector` and `serviceSelector` within a single
rule. If you attempt to set both parameters, the program will notify you of the error and require you to correct the
rule.