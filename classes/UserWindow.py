#!/usr/bin/env python3

from classes import Window, LoginInfo, AchievementsWindow
import pytermgui as ptg
from typing import Dict


class UserWindow(Window.Window):
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        self.loginInstance = LoginInfo.LoginInfo.instance()
        self.manager = manager
        self.namespace = ptg.Window(
            ptg.Label(
                "[title]Bem vindo " +
                self.loginInstance.getInfo()["nome"]
            ),
            *[
                ptg.Button(label="Área de administração", id="btnAdmin")
                for _ in (
                    range(1)
                    if self.loginInstance.getInfo()["administrador"]
                    else []
                )
            ],
            ptg.Container(
                ptg.Splitter(
                    ptg.Label("RP:"),
                    ptg.Label(
                        f"{self.loginInstance.getInfo()['rp']}"
                    ),
                ),
                ptg.Splitter(
                    ptg.Label("Email:"),
                    ptg.Label(
                        f"{self.loginInstance.getInfo()['email']}"
                    ),
                ),
                ptg.Splitter(
                    ptg.Label("Bio:"),
                    ptg.Label(
                        f"{self.loginInstance.getInfo()['bio']}"
                    ),
                ),
            ),
            ptg.Button(label="Meus achievements", id="btnAchievements"),
            ptg.Button(label="Sair", id="btnQuit"),
        )
        self.btnQuit = ptg.get_widget("btnQuit")
        self.btnQuit.onclick = lambda *_: self.userQuit()
        self.btnAchievements = ptg.get_widget("btnAchievements")
        self.btnAchievements.onclick = lambda *_: self.userAchiev()

    def userQuit(self):
        self.loginInstance.logout()
        self.namespace.close()

    def userAchiev(self):
        self.manager.add(
            AchievementsWindow
            .AchievementsWindow(self.manager)
            .getNamespace()
            .center()
        )
        return

    def getNamespace(self) -> ptg.WidgetNamespace:
        return self.namespace

    @property
    def buttons(self) -> Dict[str, ptg.Widget]:
        return self._buttons
