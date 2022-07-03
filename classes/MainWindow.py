#!/usr/bin/env python3

from classes import Window, LoginWindow
import pytermgui as ptg
from typing import Dict


class MainWindow(Window.Window):
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        self.manager = manager
        self.namespace = super().loadNamespace("Main")
        self.loginBtn = ptg.get_widget("loginBtn")
        self.loginBtn.onclick = lambda _: self.openLogin()
        self.exitBtn = ptg.get_widget("exitBtn")
        self.exitBtn.onclick = lambda *_: manager.stop()

    def getNamespace(self):
        return self.namespace.Main

    def openLogin(self):
        self.loginWindow = LoginWindow.LoginWindow(self.manager)
        self.loginWindow.buttons["exit"].onclick = \
            lambda _: self.loginWindow\
                          .getNamespace()\
                          .close()
        self.manager.add(self.loginWindow.getNamespace().center())
        self.getNamespace().close()

    @property
    def buttons(self) -> Dict[str, ptg.Widget]:
        return self._buttons
