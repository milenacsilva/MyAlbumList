#!/usr/bin/env python3

from classes import Window, LoginInfo, DbHandler
import pytermgui as ptg
from typing import Dict
import datetime


class AdminWindow(Window.Window):
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        self.db: DbHandler.DbHandler = DbHandler.DbHandler.instance()
        self.loginInstance = LoginInfo.LoginInfo.instance()
        self.manager = manager
        self.namespace = super().loadNamespace("Admin")
        self._buttons: Dict[str, ptg.Button] = {}
        self.buttons["btnAddAlbum"] = ptg.get_widget("btnAddAlbum")
        self.buttons["btnAddAlbum"].onclick = lambda _: self.addAlbum()
        self.buttons["btnQuitAdmin"] = ptg.get_widget("btnQuitAdmin")
        self.buttons["btnQuitAdmin"].onclick = lambda _: \
            self.getNamespace().close()

    def getNamespace(self) -> ptg.Window:
        return self.namespace.Admin

    def addAlbum(self):
        self.manager.add(self.namespace.AddAlbum.center())
        btnQuit: ptg.Button = ptg.get_widget("btnQuitAdd")
        btnQuit.onclick = lambda _: self.namespace.AddAlbum.close()
        btnDoAddAlbum: ptg.Button = ptg.get_widget("btnDoAddAlbum")
        btnDoAddAlbum.onclick = lambda _: self.doAddAlbum()

    def doAddAlbum(self):
        txtId: ptg.InputField = ptg.get_widget("txtId")
        txtName: ptg.InputField = ptg.get_widget("txtName")
        txtCapa: ptg.InputField = ptg.get_widget("txtCapa")
        txtAno: ptg.InputField = ptg.get_widget("txtAno")
        txtDuracao: ptg.InputField = ptg.get_widget("txtDuracao")
        if self.db.execute(
                "INSERT INTO album VALUES (%s, %s, %s, %s, %s);",
                [
                    txtId.value,
                    txtName.value,
                    txtCapa.value,
                    datetime.date(int(txtAno.value), 1, 1),
                    int(txtDuracao.value)
                ]
        ):
            self.db.commit()
            self.manager.add(self.namespace.PopupSuccess.center())
            btnQuit: ptg.Button = ptg.get_widget("btnQuitPopup")
            btnQuit.onclick = lambda _: self.namespace.PopupSuccess.close()
        else:
            self.manager.add(self.namespace.PopupError.center())
            btnQuit: ptg.Button = ptg.get_widget("btnQuitPopup")
            btnQuit.onclick = lambda _: self.namespace.PopupError.close()

    @property
    def buttons(self) -> Dict[str, ptg.Button]:
        return self._buttons
