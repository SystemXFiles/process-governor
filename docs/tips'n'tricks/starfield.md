## Starfield Optimization: Eliminating Stutters with Process Governor

[Русская версия](starfield.ru.md)

In this section, we'll explore tips and tricks to reduce stutters in the game Starfield by leveraging Process Governor. This utility provides an alternative to more popular solutions like Process Lasso and BES.

### Tip 1: Download and Extract Process Governor

To initiate the optimization process, start by downloading Process Governor from its [official GitHub repository](https://github.com/SystemXFiles/process-governor/releases/latest). Once the download is complete, extract the archive to a directory of your choice. If you're looking for a comprehensive overview of the utility, you can consult the [official documentation](https://github.com/SystemXFiles/process-governor#readme).

### Tip 2: Launch Process Governor and Create a Configuration

To commence using Process Governor, run the `Process Governor.exe` application with administrative privileges. This action will lead to the automatic creation of the configuration file, `config.json`.

### Tip 3: Configure Rules for the Starfield Process

Open the `config.json` file, which is generated automatically, and insert the following rule to prevent the Starfield game from utilizing the first processor core:

```json
{
    "processSelector": "starfield.exe",
    "affinity": "2-N" 
}
```

Replace "N" with the highest available core/thread number on your processor, beginning from 0.

### Tip 4: Automatic Configuration Update

If you already have the Process Governor program running, it will automatically pick up the updated configuration. Otherwise, you will need to launch Process Governor for the utility to load the new settings and apply them to Starfield.

### Enhancing Starfield Performance

With this configuration in place, you should notice a reduction in stutters while playing Starfield.