import subprocess

from constants.any import LOG


class TaskScheduler:
    """
    A class to manage tasks in Windows Task Scheduler using the schtasks utility.
    """

    @staticmethod
    def create_startup_task(task_name, exe_path):
        """
        Creates a startup task in the Task Scheduler.

        Parameters:
            task_name (str): The name of the task to be created.
            exe_path (str): The path of the executable to be run as the startup task.
        """
        command = f"schtasks /create /tn \"{task_name}\" /tr \"{exe_path}\" /sc onlogon /rl highest"

        try:
            subprocess.run(command, check=True, shell=True)
            LOG.info(f"Task '{task_name}' created successfully.")
        except subprocess.CalledProcessError as e:
            LOG.error(f"Error creating task '{task_name}': {e}. Command: {command}")
            raise

    @staticmethod
    def check_task(task_name):
        """
        Checks for the existence of a task in the Task Scheduler.

        Parameters:
            task_name (str): Name of the task.

        Returns:
            bool: True if the task exists, False otherwise.
        """
        command = f"schtasks /query /tn \"{task_name}\""

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return task_name in result.stdout
        except subprocess.CalledProcessError as e:
            LOG.error(f"Error checking task '{task_name}': {e}. Command: {command}")
            raise

    @staticmethod
    def delete_task(task_name):
        """
        Deletes a task from the Task Scheduler.

        Parameters:
            task_name (str): Name of the task.
        """
        command = f"schtasks /delete /tn \"{task_name}\" /f"

        try:
            subprocess.run(command, check=True, shell=True)
            LOG.info(f"Task '{task_name}' deleted successfully.")
        except subprocess.CalledProcessError as e:
            LOG.error(f"Error deleting task '{task_name}': {e}. Command: {command}")
            raise
