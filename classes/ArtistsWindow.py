#!/usr/bin/env python3

from classes import Window, DbHandler, LoginInfo
import pytermgui as ptg
from typing import Dict


class ArtistsWindow(Window.Window):
    def __init__(self, manager: ptg.window_manager.manager.WindowManager):
        self.manager = manager
        self.db: DbHandler.DbHandler = DbHandler.DbHandler.instance()
        self.loginInstance = LoginInfo.LoginInfo.instance()
        self.namespace = ptg.Window(
            ptg.Label("[title]Meus artists"),
            ptg.Label("[body]Quantidade de álbuns ouvidos e \
            classificados pelo usuário"),
            ptg.Container(
                ptg.Splitter(
                    ptg.Label("Nome"),
                    ptg.Label("Quantidade de álbuns ouvidos"),
                    ptg.Label("Quantidade de álbuns avaliados"),
                ),
                *[
                    ptg.Splitter(
                        ptg.Label(artist["nome"]),
                        ptg.Label(f"{artist['qnt_albuns_ouvidos']}"),
                        ptg.Label(f"{artist['qnt_albuns_avaliados']}"),
                    )
                    for artist in self.artists
                ],
            ),
            ptg.Button(
                label="Sair",
                id="btnQuitClassics"
            )
        )
        btnQuit: ptg.Button = ptg.get_widget("btnQuitClassics")
        btnQuit.onclick = lambda _: self.namespace.close()

    def getNamespace(self) -> ptg.Window:
        return self.namespace

    @property
    def artists(self):
        if not hasattr(self, "_artists"):
            self._artists = self.db.fetchAll(
                "SELECT ART.NOME, \
                COUNT(ALBUM_OUVIDO.ID_SPOTIFY) AS QNT_ALBUNS_OUVIDOS, \
                COUNT(ALBUM_AVALIADO.ID_ALBUM) AS QNT_ALBUNS_AVALIADOS \
                FROM (SELECT * FROM LISTA_PADRAO O WHERE \
                O.TAG_USUARIO = %s AND O.OUVIDOS = TRUE) O \
                JOIN ALBUM_LISTA AL ON \
                AL.TAG_USUARIO = O.TAG_USUARIO AND AL.N_LISTA = O.N_LISTA \
                JOIN ALBUM ALBUM_OUVIDO ON \
                AL.ID_ALBUM = ALBUM_OUVIDO.ID_SPOTIFY \
                JOIN ALBUM_ARTISTA AA ON \
                AA.ID_ALBUM = ALBUM_OUVIDO.ID_SPOTIFY \
                JOIN ARTISTA ART ON \
                ART.ID_SPOTIFY = AA.ID_ARTISTA \
                LEFT JOIN AVALIACAO ALBUM_AVALIADO ON \
                O.TAG_USUARIO = ALBUM_AVALIADO.TAG_USUARIO AND \
                ALBUM_OUVIDO.ID_SPOTIFY = ALBUM_AVALIADO.ID_ALBUM \
                GROUP BY (ART.NOME) \
                ORDER BY (ART.NOME);",
                [self.loginInstance.getInfo()["tag"]]
            )
        return self._artists

    @property
    def buttons(self) -> Dict[str, ptg.Widget]:
        return self._buttons
