import os
from abc import ABC
from enum import Enum
from typing import Optional, List

import psutil
from psutil import AccessDenied, NoSuchProcess
from pyuac import isUserAdmin

from configuration.config import Config
from configuration.rule import Rule
from model.process import Process
from model.service import Service
from service.processes_info_service import ProcessesInfoService
from service.services_info_service import ServicesInfoService
from util.logs import log
from util.utils import fnmatch_cached, cached


class _ProcessParameter(Enum):
    AFFINITY = "affinity"
    NICE = "nice"
    IONICE = "ionice"

    def __str__(self):
        return self.value


class RulesService(ABC):
    """
    The RulesService class provides methods for applying rules to processes and services in Process Governor.
    It is an abstract base class (ABC) to be subclassed by specific implementation classes.
    """

    __ignore_pids: set[int] = {0, os.getpid()}
    __ignored_process_parameters: dict[tuple[int, str], set[_ProcessParameter]] = {}

    @classmethod
    def apply_rules(cls, config: Config):
        """
        Apply rules from the provided configuration to processes and services.

        Args:
            config (Config): The configuration object containing the rules to be applied.
        """
        if not config.rules:
            return

        cls.__light_gc_ignored_process_parameters()

        processes: dict[int, Process] = ProcessesInfoService.get_new_processes()
        services: dict[int, Service] = ServicesInfoService.get_list()

        cls.__handle_processes(config, processes, services)

    @classmethod
    def __handle_processes(cls, config, processes, services):
        for pid, process_info in processes.items():
            if pid in cls.__ignore_pids:
                continue

            try:
                service_info: Service = ServicesInfoService.get_by_pid(pid, services)
                rule: Rule = cls.__first_rule_by_name(config.rules, service_info, process_info)

                if not rule:
                    continue

                tuple_pid_name = (pid, process_info.name)
                ignored_process_parameters = cls.__ignored_process_parameters.get(tuple_pid_name, set())
                not_success: List[_ProcessParameter] = []

                if _ProcessParameter.AFFINITY not in ignored_process_parameters:
                    cls.__set_affinity(not_success, process_info, rule)

                if _ProcessParameter.NICE not in ignored_process_parameters:
                    cls.__set_nice(not_success, process_info, rule)

                if _ProcessParameter.IONICE not in ignored_process_parameters:
                    cls.__set_ionice(not_success, process_info, rule)

                if not_success:
                    cls.__ignore_process_parameter(tuple_pid_name, set(not_success))

                    log.warning(f"Set failed [{', '.join(map(str, not_success))}] "
                                    f"for {process_info.name} ({process_info.pid}"
                                    f"{', ' + service_info.name + '' if service_info else ''}"
                                    f")")
            except NoSuchProcess as _:
                log.warning(f"No such process: {pid}")

    @classmethod
    def __set_ionice(cls, not_success, process_info, rule: Rule):
        if not rule.ioPriority or process_info.ionice == rule.ioPriority:
            return

        parameter = _ProcessParameter.IONICE

        try:
            process_info.process.ionice(rule.ioPriority)
            log.info(f"Set {parameter.value} = {rule.ioPriority} for {process_info.name} ({process_info.pid})")
        except AccessDenied as _:
            not_success.append(parameter)

    @classmethod
    def __set_nice(cls, not_success, process_info, rule: Rule):
        if not rule.priority or process_info.nice == rule.priority:
            return

        parameter = _ProcessParameter.NICE

        try:
            process_info.process.nice(rule.priority)
            log.info(f"Set {parameter.value} = {rule.priority} for {process_info.name} ({process_info.pid})")
        except AccessDenied as _:
            not_success.append(parameter)

    @classmethod
    def __set_affinity(cls, not_success, process_info, rule: Rule):
        if rule.affinity is None:
            return

        parameter = _ProcessParameter.AFFINITY
        affinity_as_list = rule.affinity_as_list()

        if process_info.affinity == affinity_as_list:
            return

        try:
            process_info.process.cpu_affinity(affinity_as_list)
            log.info(f"Set {parameter.value} = {rule.affinity} for {process_info.name} ({process_info.pid})")
        except AccessDenied as _:
            not_success.append(parameter)

    @classmethod
    def __first_rule_by_name(cls, rules: List[Rule], service: Service, process: Process) -> Optional[Rule]:
        for rule in rules:
            if service and fnmatch_cached(service.name, rule.serviceSelector):
                return rule

            if fnmatch_cached(process.name, rule.processSelector):
                return rule
        return None

    @classmethod
    def __ignore_process_parameter(cls, tuple_pid_name: tuple[int, str], parameters: set[_ProcessParameter]):
        if isUserAdmin():
            cls.__ignored_process_parameters[tuple_pid_name] = parameters

    @classmethod
    @cached(5)  # Workaround to ensure the procedure runs only once every 5 seconds
    def __light_gc_ignored_process_parameters(cls):
        pids = psutil.pids()
        remove_pids: List[tuple[int, str]] = []

        for item in cls.__ignored_process_parameters.keys():
            pid, _ = item

            if pid not in pids:
                remove_pids.append(item)

        for item in remove_pids:
            del cls.__ignored_process_parameters[item]
