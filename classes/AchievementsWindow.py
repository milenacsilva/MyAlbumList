#!/usr/bin/env python3

from classes import Window, LoginInfo, DbHandler
import pytermgui as ptg
from typing import Dict


class AchievementsWindow(Window.Window):
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        self.db: DbHandler.DbHandler = DbHandler.DbHandler.instance()
        self.loginInstance = LoginInfo.LoginInfo().instance()
        self.manager = manager
        self.namespace = ptg.Window(
            ptg.Label("[title]Meus achievements:"),
            ptg.Container(
                *[
                    ptg.Label(f"{achiev[0]}")
                    for achiev in (
                        self.achievements
                        if len(self.achievements)
                        else ["Você não possui nenhum achievement!"]
                    )
                ],
            ),
            ptg.Label("[title]Achievements a ganhar:"),
            ptg.Container(
                *[
                    ptg.Label(f"{achiev[0]}")
                    for achiev in (
                        self.remaining
                        if len(self.remaining)
                        else ["Você não possui nenhum achievement a receber!"]
                    )
                ],
            ),
            ptg.Button(label="Sair", id="btnQuit"),
        )

    def getNamespace(self) -> ptg.WidgetNamespace:
        return self.namespace

    @property
    def achievements(self):
        if not hasattr(self, "_achievements"):
            self._achievements = self.db.fetchAll(
                "SELECT nome FROM achievement_usuario WHERE tag_usuario=%s;",
                [self.loginInstance.getInfo()["user"]]
            )
        return self._achievements

    @property
    def remaining(self):
        if not hasattr(self, "_remaining"):
            self._remaining = self.db.fetchAll(
                "SELECT nome FROM achievement EXCEPT \
                (SELECT nome FROM achievement_usuario \
                WHERE tag_usuario=%s);",
                [self.loginInstance.getInfo()["user"]]
            )
        return self._remaining

    @property
    def buttons(self) -> Dict[str, ptg.Widget]:
        return self._buttons
