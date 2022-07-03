#!/usr/bin/env python3

from classes import Window, LoginInfo, UserWindow
import pytermgui as ptg
from typing import Dict


class LoginWindow(Window.Window):
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        self.loginInstance = LoginInfo.LoginInfo().instance()
        self.manager = manager
        self.namespace = super().loadNamespace("Login")
        self.loginBtn = ptg.get_widget("enterBtn")
        self.loginBtn.onclick = lambda *_: self.login()
        self.exitBtn = ptg.get_widget("backLoginBtn")
        self._buttons: Dict[str, ptg.Widget] = {}
        self._buttons["login"] = self.loginBtn
        self._buttons["exit"] = self.exitBtn

    def getNamespace(self) -> ptg.WidgetNamespace:
        return self.namespace.Login

    def login(self):
        userTxt: ptg.Widget = ptg.get_widget("userTxt")
        passTxt: ptg.Widget = ptg.get_widget("passTxt")
        if self.loginInstance.login(userTxt.value, passTxt.value):
            self.success()
        else:
            self.error()

    def success(self):
        self.successPopup = self.namespace.PopupSuccess
        self.manager.add(self.successPopup.center())
        btnSuccess: ptg.Widget = ptg.get_widget("btnSuccess")
        btnSuccess.onclick = lambda *_: self.successClose()

    def successClose(self):
        # self.successPopup.close()
        self.manager.remove(self.successPopup)
        userWindow = UserWindow.UserWindow(self.manager)
        self.manager.add(
            userWindow.getNamespace().center()
        )

    def error(self):
        self.manager.add(self.namespace.PopupError.center())
        btnError: ptg.Widget = ptg.get_widget("btnError")
        btnError.onclick = lambda *_: self.errorClose()

    def errorClose(self):
        self.namespace.PopupError.close()

    @property
    def buttons(self) -> Dict[str, ptg.Widget]:
        return self._buttons
