![Logo Process Governor](images/github-banner-readme.png)

[![EN](icons/gb.png) English version](README.md)

---

**Process Governor** - это утилита на Python, предназначенная для управления процессами и службами в Windows путем
настройки их приоритетов, приоритетов ввода/вывода и привязки к ядрам на основе пользовательских правил.

<details>
   <summary>Скриншоты</summary>

   >![tray_menu_screenshot.png](images/tray_menu_screenshot.png)
   > 
   >![audio_artiacle_rule_configurator_screenshot.png](images/audio_artiacle_rule_configurator_screenshot.png)
   > 
   >![rule_configurator_with_error_screenshot.png](images/rule_configurator_with_error_screenshot.png)
</details>

## Возможности

- Настройка приоритетов процессов и служб для повышения производительности.
- Управление приоритетами ввода/вывода для оптимизации использования ресурсов.
- Определение привязки к ядрам для процессов.
- Тонкая настройка процессов и служб Windows на основе [пользовательских правил](ui_rule_configurator.ru.md).
- Непрерывный мониторинг файла конфигурации для применения правил.
- Возможность добавить Process Governor в автозапуск.

## Начало работы

Для начала работы с **Process Governor** выполните следующие шаги:

1. Скачайте последнюю готовую сборку по
   ссылке: [Latest Release](https://github.com/SystemXFiles/process-governor/releases/latest).
2. Запустите исполняемый файл `Process Governor.exe` с **правами администратора**.
   Это важно, чтобы программа могла внести необходимые изменения в приоритеты процессов и служб, приоритеты ввода-вывода
   и соответствие ядер.
3. [Настройте правила](ui_rule_configurator.ru.md) для процессов и сервисов.

Программу можно закрыть, обратившись к значку в системном трее.

## База знаний

- [Конфигурирование правил](ui_rule_configurator.ru.md)
- [Файл конфигурации](configuration_file.ru.md)
- [Запуск из исходников и создание портабельной сборки](run_and_build.ru.md)
- **Советы и трюки**
  - [Оптимизация звука](tips'n'tricks/audio.ru.md)
  - [Оптимизация игр](tips'n'tricks/game_optimization.ru.md)

## Лицензия

Этот проект лицензирован согласно GNU General Public License v3.0 - см. файл [LICENSE](../LICENSE) для подробностей.