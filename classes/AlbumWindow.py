#!/usr/bin/env python3

from classes import Window, DbHandler  # , LoginInfo
import pytermgui as ptg
from typing import Dict
# import datetime


class AlbumsWindow(Window.Window):
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        self.db: DbHandler.DbHandler = DbHandler.DbHandler.instance()
        self.manager = manager
        # self.loginInstance = LoginInfo.LoginInfo.instance()
        self._buttons: Dict[str, ptg.Label] = {}
        self.namespace = ptg.Window()

    def getNamespace(self) -> ptg.Window:
        return self.namespace

    def setAlbum(self, id_spotify: str):
        self.album = self.db.fetchOne(
            "SELECT * FROM album WHERE id_spotify = %s;",
            [id_spotify]
        )
        self.namespace = ptg.Window(
            ptg.Label("[title]" + self.album["nome"]),
            ptg.Container(
                ptg.Splitter(
                    ptg.Label("Ano:"),
                    ptg.Label(f"{self.album['ano'].year}")
                ),
                ptg.Splitter(
                    ptg.Label("Duração:"),
                    ptg.Label(f"{self.album['duracao']}")
                ),
                ptg.Splitter(
                    ptg.Label("ID Spotify:"),
                    ptg.Label(f"{self.album['id_spotify']}")
                ),
            ),
            ptg.Button(label="Sair", id="btnQuitAlbum")
        )
        self.buttons["btnQuitAlbum"] = ptg.get_widget("btnQuitAlbum")
        self.buttons["btnQuitAlbum"].on_click = lambda _: \
            self.getNamespace().close()

    @property
    def buttons(self) -> Dict[str, ptg.Widget]:
        return self._buttons
