#!/usr/bin/env python3

import pytermgui as ptg
from classes import MainWindow


PTG_CONFIG = """\
config: {}

markup:
    title: 210 bold
    body: 245 italic
"""


class Interface():
    _instance = None

    def __init__(self):
        self.manager = ptg.WindowManager()
        self.loader = ptg.YamlLoader()
        self.loader.load(PTG_CONFIG)
        self.main = MainWindow.MainWindow(self.manager)
        self.mainWin = self.main.getNamespace().center()
        self.mainWin.bind(ptg.keys.ESC, lambda window, _: self.manager.stop())
        self.manager.add(self.mainWin)
        self.manager.run()

    def kill(self):
        self.manager.stop()
        self._instance = None

    def __del__(self):
        if not self.manager:
            pass
        self.manager.stop()
        del self.manager

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
