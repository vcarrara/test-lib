import logging
from typing import Union


class OlympusLogger(logging.Logger):
    def __init__(self,
                 level: Union[str, int] = logging.DEBUG,
                 name: str = 'OLYMPUS_LOGGER',
                 format: str = '%(asctime)s | %(levelname)s | %(message)s',
                 log_to_stdout: bool = True,
                 log_to_file: bool = False,
                 file_path: Union[str, None] = None
                 ) -> None:

        super().__init__(name=name, level=level)

        if log_to_file and file_path is None:
            raise ValueError('file_path must be set when log_to_file is True, received: None')

        if log_to_stdout:
            stream_handler = logging.StreamHandler()
            formatter = logging.Formatter(format)
            stream_handler.setFormatter(formatter)
            self.addHandler(stream_handler)

        if log_to_file:
            file_handler = logging.FileHandler(file_path)
            formatter = logging.Formatter(format)
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)
