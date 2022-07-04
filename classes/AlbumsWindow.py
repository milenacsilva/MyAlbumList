#!/usr/bin/env python3

from classes import Window, LoginInfo, DbHandler, AlbumWindow
import pytermgui as ptg
from typing import Dict
import urllib.parse


class AlbumsWindow(Window.Window):
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        self.db: DbHandler.DbHandler = DbHandler.DbHandler.instance()
        self.manager = manager
        self.loginInstance = LoginInfo.LoginInfo.instance()
        self._buttons: Dict[str, ptg.Label] = {}
        self.namespace = ptg.Window(
            ptg.Label("[title]Álbums"),
            ptg.Label("[body]*: Ouvidos"),
            ptg.Container(
                *[
                    ptg.Label(
                        value=album['nome'] +
                        ('*' if album['tag_usuario'] is not None else ''),
                        id=f"lbl{urllib.parse.quote(album['nome'])}"
                    )
                    for album in self.albums
                ],
            ),
            ptg.Label(),
            ptg.Button(label="Sair", id="btnQuitAlbums"),
        )
        for album in self.albums:
            lblName = f"lbl{urllib.parse.quote(album['nome'])}"
            self._buttons[lblName] = ptg.get_widget(lblName)
            self._buttons[lblName].on_click = lambda _, \
                _id=album['id_spotify']: self.openAlbum(_id)
        self.btnQuit: ptg.Button = ptg.get_widget("btnQuitAlbums")
        self.btnQuit.onclick = lambda *_: self.getNamespace().close()

    def openAlbum(self, _id: str):
        albumWin = AlbumWindow.AlbumsWindow(self.manager)
        albumWin.setAlbum(_id)
        self.manager.add(albumWin.getNamespace().center())

    def getNamespace(self) -> ptg.Window:
        return self.namespace

    @property
    def albums(self):
        if not hasattr(self, "_albums"):
            self._albums = self.db.fetchAll(
                "SELECT A.id_spotify, A.nome, AL.tag_usuario FROM album A LEFT JOIN\
                album_lista AL ON AL.tag_usuario = %s\
                AND A.id_spotify = AL.id_album\
                GROUP BY A.id_spotify, A.nome, AL.tag_usuario;",
                [self.loginInstance.getInfo()["tag"]]
            )
        return self._albums

    @property
    def buttons(self) -> Dict[str, ptg.Widget]:
        return self._buttons
