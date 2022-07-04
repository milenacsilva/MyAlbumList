#!/usr/bin/env python3

from classes import Window, DbHandler
import pytermgui as ptg
from typing import Dict


class SingleAchievementWindow(Window.Window):
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        self.manager = manager
        self.db: DbHandler.DbHandler = DbHandler.DbHandler.instance()
        self.namespace: ptg.WidgetNamespace = \
            super().loadNamespace("Achievement")
        self.lblName: ptg.Label = ptg.get_widget("lblName")
        self.cntAchiev: ptg.Container = ptg.get_widget("cntAchiev")
        self.btnQuitAchiev = ptg.get_widget("btnQuitAchiev")
        self.btnQuitAchiev.onclick = lambda *_: self.getNamespace().close()

    def setAchievement(self, nome: str, remaining: bool = False):
        self.lblName.value = f"[title]{nome}"
        self.achievement = self.db.fetchOne(
            "SELECT * FROM achievement WHERE nome = %s",
            [nome]
        )
        self.cntAchiev.set_widgets([
            ptg.Label(self.achievement["descricao"]),
            ptg.Label(f"Recompensa: {self.achievement['reward']}"),
        ])

    def getNamespace(self) -> ptg.Window:
        return self.namespace.Achievement

    @property
    def buttons(self) -> Dict[str, ptg.Widget]:
        return self._buttons
