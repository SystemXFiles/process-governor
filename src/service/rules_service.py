import os
from abc import ABC
from typing import Optional, Callable

import psutil
from psutil import AccessDenied, NoSuchProcess

from configuration.config import Config
from configuration.rule import ProcessRule, ServiceRule
from constants.log import LOG
from enums.bool import BoolStr
from enums.io_priority import to_iopriority
from enums.priority import to_priority
from enums.process import ProcessParameter
from enums.selector import SelectorType
from model.process import Process
from service.processes_info_service import ProcessesInfoService
from util.cpu import format_affinity
from util.decorators import cached
from util.scheduler import TaskScheduler
from util.utils import path_match


class RulesService(ABC):
    """
    The RulesService class provides methods for applying rules to processes and services.
    """

    __ignore_pids: set[int] = {0, os.getpid()}
    __ignored_process_parameters: dict[Process, set[ProcessParameter]] = {}

    @classmethod
    def apply_rules(cls, config: Config, only_new: bool):
        """
        Apply the rules defined in the configuration to handle processes and services.

        Args:
            config (Config): The configuration object containing the rules.
            only_new (bool, optional): If set to True, all processes will be fetched, regardless of their status.

        Returns:
            None
        """
        if not (config.serviceRules or config.processRules):
            return

        cls.__light_gc_ignored_process_parameters()
        cls.__handle_processes(config, ProcessesInfoService.get_processes(), only_new)

    @classmethod
    def __handle_processes(
        cls, config: Config, processes: dict[int, Process], only_new: bool
    ):
        for pid, process in processes.items():
            if pid in cls.__ignore_pids:
                continue

            rule: Optional[ProcessRule | ServiceRule] = cls.__first_rule_by_process(
                config, process
            )

            if not rule:
                continue

            if rule.force == BoolStr.NO and only_new and not process.is_new:
                continue

            if rule.delay > 0:
                TaskScheduler.schedule_task(
                    process, cls.__handle_process, process, rule, delay=rule.delay
                )
            else:
                cls.__handle_process(process, rule)

    @classmethod
    def __handle_process(cls, process: Process, rule: ProcessRule | ServiceRule):
        parameter_methods: dict[
            ProcessParameter,
            tuple[Callable[[Process, ProcessRule | ServiceRule], bool], str],
        ] = {
            ProcessParameter.AFFINITY: (
                cls.__set_affinity,
                format_affinity(rule.affinity),
            ),
            ProcessParameter.NICE: (cls.__set_nice, rule.priority),
            ProcessParameter.IONICE: (cls.__set_ionice, rule.ioPriority),
        }

        try:
            ignored_parameters = cls.__ignored_process_parameters.setdefault(
                process, set()
            )

            for param, (method, logger_value) in parameter_methods.items():
                if param in ignored_parameters:
                    continue

                service_name = f", {process.service_name}" if process.service else ""
                logger_string = f"{param.value} `{logger_value}` for {process.process_name} ({process.pid}{service_name})"

                try:
                    if method(process, rule):
                        LOG.info(f"Set {logger_string}.")
                except AccessDenied:
                    ignored_parameters.add(param)
                    LOG.warning(f"Failed to set {logger_string}.")

        except NoSuchProcess:
            pass

    @classmethod
    def __set_ionice(cls, process: Process, rule: ProcessRule | ServiceRule):
        io_priority = to_iopriority[rule.ioPriority]

        if io_priority and process.io_priority != io_priority:
            process.process.ionice(io_priority)
            return True

    @classmethod
    def __set_nice(cls, process: Process, rule: ProcessRule | ServiceRule):
        priority = to_priority[rule.priority]

        if priority and process.priority != priority:
            process.process.nice(priority)
            return True

    @classmethod
    def __set_affinity(cls, process: Process, rule: ProcessRule | ServiceRule):
        if rule.affinity and process.affinity != rule.affinity:
            process.process.cpu_affinity(rule.affinity)
            return True

    @classmethod
    def __first_rule_by_process(
        cls, config: Config, process: Process
    ) -> Optional[ProcessRule | ServiceRule]:
        if process.service:
            for rule in config.serviceRules:
                if path_match(rule.selector, process.service_name):
                    return rule

        for rule in config.processRules:
            value = cls._get_value_for_matching(process, rule)

            if path_match(rule.selector, value):
                return rule

        return None

    @classmethod
    def find_rules_ids_by_process(
        cls,
        process: Process,
        process_rules: dict[str, ProcessRule],
        service_rules: dict[str, ServiceRule],
    ) -> list[tuple[str, ProcessRule | ServiceRule]]:
        result = []

        if process.service:
            for row_id, rule in service_rules.items():
                if path_match(rule.selector, process.service_name):
                    result.append((row_id, rule))

        for row_id, rule in process_rules.items():
            value = cls._get_value_for_matching(process, rule)

            if path_match(rule.selector, value):
                result.append((row_id, rule))

        return result

    @classmethod
    def _get_value_for_matching(cls, process, rule):
        if rule.selectorBy == SelectorType.NAME:
            return process.process_name
        elif rule.selectorBy == SelectorType.PATH:
            return process.bin_path
        elif rule.selectorBy == SelectorType.CMDLINE:
            return process.cmd_line

        message = f"Unknown selector type: {rule.selectorBy}"
        LOG.error(message)
        raise ValueError(message)

    @classmethod
    @cached(5)  # Workaround to ensure the procedure runs only once every 5 seconds
    def __light_gc_ignored_process_parameters(cls) -> None:
        pids = psutil.pids()
        # Create a copy of the items to iterate over, preventing modification issues
        current_items = list(cls.__ignored_process_parameters.items())
        cls.__ignored_process_parameters = {
            key: value for key, value in current_items if key.pid in pids
        }
