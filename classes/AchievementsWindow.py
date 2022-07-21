#!/usr/bin/env python3

from classes import Window, LoginInfo, DbHandler, SingleAchievementWindow
import pytermgui as ptg
from typing import Dict
import urllib.parse


class AchievementsWindow(Window.Window):
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        self.db: DbHandler.DbHandler = DbHandler.DbHandler.instance()
        self.loginInstance: LoginInfo.LoginInfo = LoginInfo.LoginInfo()\
                                                           .instance()
        self.loginInstance.updateAchievements()
        self._buttons = {}
        self.manager = manager
        self.namespace = ptg.Window(
            ptg.Label("[title]Meus achievements:"),
            ptg.Container(
                *[
                    ptg.Label(f"{achiev['nome']}")
                    for achiev in (
                        self.achievements
                        if len(self.achievements)
                        else [{'nome': "Você não possui nenhum \
                        achievement."}]
                    )
                ],
            ),
            ptg.Label("[title]Achievements a ganhar:"),
            ptg.Container(
                *[
                    ptg.Label(
                        f"{achiev['nome']}",
                        id=urllib.parse.quote(achiev['nome'])
                    )
                    for achiev in (
                        self.remaining
                        if len(self.remaining)
                        else [{'nome': "Você não possui nenhum \
                        achievement a receber!"}]
                    )
                ],
            ),
            ptg.Button(label="Sair", id="btnQuit"),
        )
        for achiev in self.remaining:
            name: str = achiev['nome'][::-1][::-1]
            parsedName: str = urllib.parse.quote(name)
            self._buttons[f"btn{parsedName}"] = \
                ptg.get_widget(parsedName)
            self._buttons[f"btn{parsedName}"]\
                .on_click = lambda _, nome=name: self.openAchievement(nome)
        self.btnQuit = ptg.get_widget("btnQuit")
        self.btnQuit.onclick = lambda *_: self.namespace.close()

    def getNamespace(self) -> ptg.Window:
        return self.namespace

    @property
    def achievements(self):
        if not hasattr(self, "_achievements"):
            self._achievements = self.db.fetchAll(
                "SELECT nome FROM achievement_usuario WHERE tag_usuario=%s;",
                [self.loginInstance.getInfo()["tag"]]
            )
        return self._achievements

    def openAchievement(self, nome: str):
        achievWindow = SingleAchievementWindow\
            .SingleAchievementWindow(self.manager)
        achievWindow.setAchievement(nome)
        self.manager.add(
            achievWindow.getNamespace().center()
        )

    @property
    def remaining(self):
        if not hasattr(self, "_remaining"):
            self._remaining = self.db.fetchAll(
                "SELECT nome FROM achievement EXCEPT \
                (SELECT nome FROM achievement_usuario \
                WHERE tag_usuario=%s);",
                [self.loginInstance.getInfo()["tag"]]
            )
        return self._remaining

    @property
    def buttons(self) -> Dict[str, ptg.Widget]:
        return self._buttons
