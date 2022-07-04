#!/usr/bin/env python3

import logging


class Logger():
    _instance = None

    def __init__(self):
        Log_Format = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(
            filename="logfile.log",
            filemode="w",
            format=Log_Format,
            level=logging.ERROR
        )
        self._logger = logging.getLogger()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def logger(self) -> logging.Logger:
        return self._logger
