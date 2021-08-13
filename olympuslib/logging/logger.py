import logging
from typing import Union


class OlympusLogger(logging.Logger):
    """
    Custom logger for Olympus data pipeline. The class extends the logging.Logger class and wraps some of its capacities throughout a custom constructor.
    """

    def __init__(self,
                 level: Union[str, int] = logging.DEBUG,
                 name: str = 'OLYMPUS_LOGGER',
                 format: str = '%(asctime)s | %(levelname)s | %(message)s',
                 log_to_stdout: bool = True,
                 log_to_file: bool = False,
                 file_path: Union[str, None] = None
                 ) -> None:
        """Constructor

        Args:
            level (Union[str, int], optional): Threshold from which logging is effective. Defaults to logging.DEBUG.
            name (str, optional): Name of the logger. Defaults to 'OLYMPUS_LOGGER'.
            format (str, optional): Format string of the logs. Defaults to '%(asctime)s | %(levelname)s | %(message)s'.
            log_to_stdout (bool, optional): Whether the logger should log to stdout or not. Defaults to True.
            log_to_file (bool, optional): Whether the logger should log to a file or not. Defaults to False.
            file_path (Union[str, None], optional): Path of the file in which logs will be written by the logger. Defaults to None.

        Raises:
            ValueError: A ValueError is raised if parameter log_to_file is True but file_path is unset.
        """

        super().__init__(name=name, level=level)

        if log_to_file and file_path is None:
            raise ValueError('file_path must be set when log_to_file is True, received: None')

        if log_to_stdout:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            formatter = logging.Formatter(format)
            stream_handler.setFormatter(formatter)
            self.addHandler(stream_handler)

        if log_to_file:
            file_handler = logging.FileHandler(file_path)
            file_handler.setLevel(level)
            formatter = logging.Formatter(format)
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)
