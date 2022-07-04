#!/usr/bin/env python3

from classes import Window, LoginInfo, AchievementsWindow, AlbumsWindow, AdminWindow
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
                    if self.loginInstance.getInfo()["eh_administrador"]
                    else []
                )
            ],
            ptg.Container(
                ptg.Splitter(
                    ptg.Label("RP:"),
                    ptg.Label(
                        f"{self.loginInstance.getInfo()['rockpoints']}"
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
            ptg.Label(),
            ptg.Button(label="Meus achievements", id="btnAchievements"),
            ptg.Button(label="Todos os álbuns", id="btnAlbums"),
            ptg.Label(),
            ptg.Button(label="Sair", id="btnQuit"),
        )
        self.btnQuit: ptg.Button = ptg.get_widget("btnQuit")
        self.btnQuit.onclick = lambda *_: self.userQuit()
        self.btnAchievements: ptg.Button = ptg.get_widget("btnAchievements")
        self.btnAchievements.onclick = lambda *_: self.userAchiev()
        self.btnAlbums: ptg.Button = ptg.get_widget("btnAlbums")
        self.btnAlbums.onclick = lambda _: self.openAlbums()
        if self.loginInstance.getInfo()["eh_administrador"]:
            self.btnAdmin: ptg.Button = ptg.get_widget("btnAdmin")
            self.btnAdmin.onclick = lambda _: self.openAdmin()

    def userQuit(self):
        self.loginInstance.logout()
        self.namespace.close()

    def openAdmin(self):
        self.manager.add(
            AdminWindow
            .AdminWindow(self.manager)
            .getNamespace()
            .center()
        )

    def userAchiev(self):
        self.manager.add(
            AchievementsWindow
            .AchievementsWindow(self.manager)
            .getNamespace()
            .center()
        )

    def getNamespace(self) -> ptg.Window:
        return self.namespace

    def openAlbums(self):
        self.manager.add(
            AlbumsWindow.AlbumsWindow(self.manager)
            .getNamespace()
            .center()
        )

    @property
    def buttons(self) -> Dict[str, ptg.Widget]:
        return self._buttons
