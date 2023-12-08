![Logo Process Governor](../images/sound-theme-header.png)

# Optimizing Audio using Process Governor

[![README](../icons/readme.png) README](../README.md) | [![RU](../icons/ru.png) Русская версия](audio.ru.md)

---

> **Foreword:**
>
> If you are involved in music, streaming, or simply aim for perfect sound in Discord or at work, and you use real-time
> sound processing, this article is for you. It will discuss methods of system optimization to prevent sound problems
> such as stuttering or crackling under high CPU load. The proposed approach will help you configure CPU resources so
> that audio processes are prioritized and do not suffer from competition with other tasks.

## Introduction

In this article, we will explore the process of optimizing audio on a computer using the **Process Governor** tool. This
method allows for improved audio stability and reduced stuttering and crackling, especially during high processor loads.

## Background of the Issue

### Initial Situation

My story began with audio instability on my computer, particularly when I was actively using real-time audio processing.
Stuttering and crackling became the norm during online performances and applications that processed audio through
multiple audio effects. This was not only annoying but also affected the quality of my audio projects.

### Searching for a Solution

I started looking for ways to address this problem. It involved experimenting with audio interface settings, optimizing
operating system parameters, and even reinstalling audio drivers. Some of these methods led to temporary improvements,
but as the number of audio effects and sound processors increased, the problem resurfaced.

### A Radical and Effective Solution

To find a more radical and reliable solution, I came up with the idea of redistributing my PC's computing resources. I
hypothesized that allocating specific processor cores to handle audio signals and the remaining cores for regular tasks
would help solve the problem. This should ensure stable audio playback even during high CPU loads.

As a result, I manually reassigned audio processes to dedicated CPU cores and conducted testing. This proved to be an
effective solution. However, to simplify and automate this process, I decided to create a specialized application
capable of managing the distribution of processor resources between audio processes and other tasks.

### The Birth of Process Governor

From this need, the idea of creating a program capable of managing Windows processes and their CPU core assignments was
born. This gave rise to Process Governor. With its help, I could optimize audio processes and services by setting them
to run with high priority in real-time mode and assigning them to specific CPU cores. This ensured stable and
high-quality audio playback even in demanding scenarios.

## Processes and Services Affecting Audio

To process audio, I use the following programs:

1. **Voicemeeter** - a virtual mixer.
2. **Equalizer APO** - for processing sound on Voicemeeter's output devices (headphones and speakers).
3. **Kushview Element** - DAW for processing sound on Voicemeeter's input devices (microphone).

Additionally, there are Windows services and processes that interact with audio and are common to all Windows users:

1. **AudioSrv** service.
2. **AudioEndpointBuilder** service.
3. **Audiodg.exe** process.

## Preparing for Configuration

### List of Processes and Services

To set up the configuration, I created a list of processes and services responsible for handling audio:

1. **voicemeeter8x64.exe** - Voicemeeter.
2. **voicemeeterclient.exe** - The Equalizer APO process for integration with Voicemeeter.
3. **element.exe** - Kushview Element.
4. **Audiodg.exe**.
5. **AudioSrv** service.
6. **AudioEndpointBuilder** service.

### Distribution of Processor Resources

> **Note:**
>
> 1. Process Governor perceives threads as CPU cores. So when we talk about cores, remember that it includes threads.
> 2. CPU core numbering starts from 0.

I have a processor with 12 cores (24 threads), and I propose the following resource distribution:

1. The first 8 cores/16 threads are dedicated to all processes except for audio (from thread 0 to thread 15).
2. The last 4 cores/8 threads are reserved for audio (from thread 16 to thread 23).

I also recommend setting the maximum priority - real-time - for all processes responsible for audio.

> **Note:**
>
> Through trial and error, I found that changing core affinity for the services:
> 1. **AudioSrv**;
> 2. **AudioEndpointBuilder**.
>
> Leads to worsening audio issues. Therefore, for these services, I only change the priority and leave the core affinity
> untouched.

## Configuring Process Governor

<details>
   <summary><u>The old method of configuration through the configuration file.</u></summary>

> ### Preliminary Setup
>
> Before starting the setup, familiarize yourself with the installation and initial configuration instructions for
> **Process Governor** through the configuration file, available in the sections:
>
> - [Getting Started](../README.md#getting-started)
> - [Configuration File](../configuration_file.md)
>
> ### Configuration File
>
> Based on the README and the configuration file information, I propose the following `config.json` file
> for Process Governor:
>
> ```json
> {
>   "ruleApplyIntervalSeconds": 1,
>   "logging": {
>     "enable": true,
>     "level": "INFO",
>     "maxBytes": 1024,
>     "backupCount": 1
>   },
>   "rules": [
>     {
>       "processSelector": "voicemeeter8x64.exe",
>       "priority": "Realtime",
>       "affinity": "16-23"
>     },
>     {
>       "processSelector": "voicemeeterclient.exe",
>       "priority": "Realtime",
>       "affinity": "16-23"
>     },
>     {
>       "processSelector": "element.exe",
>       "priority": "Realtime",
>       "affinity": "16-23"
>     },
>     {
>       "processSelector": "Audiodg.exe",
>       "priority": "Realtime",
>       "affinity": "16-23"
>     },
>     {
>       "serviceSelector": "AudioSrv",
>       "priority": "Realtime"
>     },
>     {
>       "serviceSelector": "AudioEndpointBuilder",
>       "priority": "Realtime"
>     },
>     {
>       "processSelector": "*",
>       "affinity": "0-15"
>     }
>   ]
> }
> ```
>
> > **The key aspects to note:**
> >
> > - Processes and services responsible for audio are specified in the `serviceSelector` and `processSelector`.
> > - The "real-time" priority is set for all audio-related processes: `"priority": "Realtime"`.
> > - CPU core assignments for various scenarios are specified in: `"affinity": "<core numbers>"`.
> > - For services, CPU cores are intentionally not specified, only priority is set.
> >
> > Also, pay attention to the last rule and its `processSelector`:
> >
> > ```json
> > {
> >   "processSelector": "*",
> >   "affinity": "0-15"
> > }
> > ```
> >
> > Here, the selector is `*`, indicating that ANY process will be subject to the rule specifying cores 0-15. Since
> > rules in Process Governor are executed in order until the first match is found, this rule will only apply to
> > processes not related to audio, automatically assigning them to cores 0-15.
>
> ### Running Process Governor
>
> To apply the settings, place the `config.json` configuration file next to the Process Governor program and run it. The
> program will run in the background, regularly applying rules to new processes and is accessible from the system tray.
</details>

### Preliminary Setup

Before starting the setup, familiarize yourself with the installation and initial configuration instructions for
**Process Governor**, available in the sections:

- [Getting Started](../README.md#getting-started)
- [Configuring Rules](../ui_rule_configurator.md)

To ensure **Process Governor** automatically starts with Windows, follow these steps:

1. Launch the **Process Governor**.
2. Click on the application icon <u>in the system tray</u> to open the menu.
3. Enable the **Run on Startup** option.

Example of the enabled **Run on Startup** option:

![tray_menu_screenshot.png](../images/tray_menu_screenshot.png)

### Creating Rules

#### Opening the Rule Configurator

1. Launch **Process Governor** if it is not already running.
2. Click on the application icon <u>in the system tray</u> to open the menu.
3. Select the **Configure Rules** option to open the rule configurator.

#### Adding a Rule for process Voicemeeter

1. In the rule configurator interface, press the **Add** button to add a new rule.
2. Enter the corresponding values in the columns:
    - **Process Selector:** `voicemeeter8x64.exe`
    - **Priority:** `Realtime`
    - **Affinity:** `16-23`

#### Adding a Rule for service AudioSrv

1. Press the **Add** button.
2. Enter the corresponding values in the columns:
    - **Service Selector:** `AudioSrv`
    - **Priority:** `Realtime`

#### Adding Other Rules

Similarly, add the remaining rules in accordance with the screenshot:

![audio_artiacle_rule_configurator_screenshot.png](../images/audio_artiacle_rule_configurator_screenshot.png)

> **The key aspects to note:**
>
> - Processes and services responsible for audio are specified in the **Process Selector** and **Service Selector**.
> - The "real-time" priority is set for all audio-related processes: `Realtime`.
> - CPU core assignments for various scenarios are specified.
> - For services, CPU cores are intentionally not specified, only priority is set.
>
> Also, pay attention to the last rule and its **Process Selector**.
> Its selector is set to `*`, indicating that ANY process will be subject to the rule specifying cores 0-15. Since rules
> in Process Governor are executed in order until the first match is found, this rule will only apply to processes not
> related to audio, automatically assigning them to cores `0-15`.

### Saving the Settings

Once all the rules are configured, save them by pressing the **Save** button. Then you can close the rule configurator.
After that, the program will regularly apply the rules to the corresponding processes and manage PC resources.

## Conclusion

Configuring Process Governor provides a powerful means of optimizing audio on my PC, enhancing its stability and
quality. I hope this article helps you achieve better results in audio processing.