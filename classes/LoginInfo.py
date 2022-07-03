#!/usr/bin/env python3

from classes import DbHandler
from typing import Dict, Union, List


class LoginInfo():
    _instance = None

    def __init__(self):
        self.db: DbHandler.DbHandler = DbHandler.DbHandler.instance()

        self.info: Dict[str, any] = {
            "user": None,
            "nome": None,
            "perfil": None,
            "bio": None,
            "email": None,
            "passwrd": None,
            "genero": None,
            "dataNasc": None,
            "rp": None,
            "cidade": None,
            "estado": None,
            "pais": None,
            "critico": None,
            "administrador": None,
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
        return self.login(self.info["user"], self.info["passwrd"])

    def getInfo(self) -> Union[bool, Dict[str, any]]:
        if not self.logged:
            return False
        else:
            return self.info

    def _setInfo(self, values: Union[None, List[any]]) -> None:
        infoKeys = list(self.info.keys())
        if values is None:
            self.logged = False
            for key in infoKeys:
                self.info[key] = None
        else:
            self.logged = True
            for key, idx in list(zip(infoKeys, range(len(values)))):
                self.info[key] = values[idx]

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
