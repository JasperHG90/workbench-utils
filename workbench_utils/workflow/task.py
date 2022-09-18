import logging

from abc import ABC, abstractmethod

logger = logging.getLogger("{{ cookiecutter.module_name }}.utils.task")


class Task(ABC):
    """
    This is an abstract class that provides handy interfaces to implement workloads (e.g. jobs or job tasks).
    Create a child from this class and implement the abstract launch method.
    Class provides access to the following useful objects:
    * self.spark is a SparkSession
    * self.dbutils provides access to the DBUtils
    * self.logger provides access to the Spark-compatible logger
    * self.conf provides access to the parsed configuration of the job
    """

    def __init__(self):
        self.logger = self._prepare_logger()

    def _prepare_logger(self):
        return logging.getLogger("{{ cookiecutter.module_name }}.utils.task." + self.__class__.__name__)

    @abstractmethod
    def launch(self):
        """
        Main method of the job.
        :return:
        """
        pass
