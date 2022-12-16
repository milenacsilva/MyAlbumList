#!/usr/bin/env python3

from classes import DbHandler
from typing import Dict, Union, List


class LoginInfo():
    _instance = None

    def __init__(self):
        self.db: DbHandler.DbHandler = DbHandler.DbHandler.instance()

        self.info: Dict[str, any] = {
            "tag": None,
            "nome": None,
            "foto_perfil": None,
            "bio": None,
            "email": None,
            "senha": None,
            "genero": None,
            "data_nasc": None,
            "rockpoints": None,
            "cidade": None,
            "estado": None,
            "pais": None,
            "eh_critico": None,
            "eh_administrador": None,
        }
        self.logged = False

    def login(self, user: str, pss: str) -> bool:
        values = self.db.fetchOne(
            "SELECT * FROM USUARIO WHERE TAG = %s AND SENHA = %s;",
            [user, pss]
        )
        if values is None:
            self._setInfo(None)
        else:
            self._setInfo(values)
        return self.logged

    def logout(self):
        self._setInfo(None)

    def updateInfo(self) -> bool:
        if not self.logged:
            return
        return self.login(self.info["user"], self.info["password"])

    def getInfo(self) -> Union[bool, Dict[str, any]]:
        if not self.logged:
            return False
        else:
            return self.info

    def updateAchievements(self):
        achievsAlbumAdd = self.db.fetchAll(
            """
            SELECT Q.* FROM
            (SELECT DISTINCT APA.NOME FROM ACHIEVEMENT_POR_ALBUM APA
                WHERE NOT EXISTS (
                (SELECT A.ID_ALBUM FROM ACHIEVEMENT_POR_ALBUM A WHERE A.NOME = APA.NOME)
                EXCEPT
                (SELECT AL.ID_ALBUM FROM ALBUM_LISTA AL WHERE AL.TAG_USUARIO = %s AND AL.N_LISTA = 1)
            )) Q
            EXCEPT
            (SELECT A.NOME FROM ACHIEVEMENT_USUARIO A
            JOIN ACHIEVEMENT_POR_ALBUM APA
                ON APA.NOME = A.NOME AND A.TAG_USUARIO = %s);
            """,
            [self.info["tag"], self.info["tag"]]
        )
        achievsGeneroAdd = self.db.fetchAll(
            """
            SELECT Q.* FROM
            (SELECT APG.NOME FROM ACHIEVEMENT_POR_GENERO APG
                JOIN (SELECT AG.ID_GENERO AS GENERO, COUNT(AG.ID_GENERO) AS QTD FROM ALBUM_LISTA AL
                        JOIN ALBUM_GENERO AG
                            ON AG.ID_ALBUM = AL.ID_ALBUM
                        WHERE AL.N_LISTA=1 AND AL.TAG_USUARIO = %s
                        GROUP BY AG.ID_GENERO) QPG
                ON QPG.GENERO = APG.ID_GENERO
                WHERE QPG.QTD >= APG.QUANTIDADE) AS Q
            EXCEPT
            (SELECT A.NOME FROM ACHIEVEMENT_USUARIO A
                JOIN ACHIEVEMENT_POR_GENERO APG
                    ON APG.NOME = A.NOME AND A.TAG_USUARIO = %s);
            """,
            [self.info["tag"], self.info["tag"]]
        )
        for achiev in [*achievsAlbumAdd, *achievsGeneroAdd]:
            self.db.execute(
                "INSERT INTO ACHIEVEMENT_USUARIO VALUES (%s, %s);",
                [self.info["tag"], achiev["nome"]]
            )
        self.db.commit()

    def _setInfo(self, values: Union[None, List[any]]) -> None:
        infoKeys = list(self.info.keys())
        if values is None:
            self.logged = False
            for key in infoKeys:
                self.info[key] = None
        else:
            self.logged = True
            self.info = values

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
