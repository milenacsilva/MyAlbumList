#!/usr/bin/env python3

import psycopg2
import psycopg2.extras
from typing import List, Union, Dict
from dotenv import dotenv_values
import os
from classes import Interface, Logger


class DbHandler():
    _instance = None
    running = False

    def __init__(self):
        self.lastCommand = None
        self.lastParams = None
        try:
            env = dotenv_values(os.path.join(
                os.path.dirname(__file__),
                "..",
                ".env"
            ))
            self.conn = psycopg2.connect(
                dbname=env["DB"],
                user=env["USER"],
                host=env["HOST"],
                port=env["PORT"],
                password=env["PASS"]
            )
            self.cur = self.conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )
            self.running = True
        except Exception as e:
            Interface.Interface.instance().kill()
            Logger.Logger.instance()\
                         .logger\
                         .warning("Erro na conexão com o banco de dados!")
            Logger.Logger.instance()\
                         .logger\
                         .error(f"Erro de conexão com o DB: {e}")

    def fetchOne(
            self,
            query: str,
            params: Union[Dict[str, str], List[str]]
    ) -> Dict[str, any]:
        self.execute(query, params)
        return self.cur.fetchone()

    def fetchAll(
            self,
            query: str,
            params: Union[Dict[str, str], List[str]]
    ) -> List[Dict[str, any]]:
        self.execute(query, params)
        return self.cur.fetchall()

    def execute(
            self,
            query: str,
            params: Union[Dict[str, str], List[str]]
    ) -> bool:
        self.lastCommand = query
        self.lastParams = params
        try:
            self.cur.execute(query, params)
            return True
        except Exception as e:
            import sys
            print("AAA", e, file=sys.stderr)
            Logger.Logger.instance().logger.error(f"SQL Error: \t{e}")
            return False

    def commit(self):
        self.conn.commit()
        return

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __del__(self):
        if not self.running:
            return
        self.cur.close()
        self.conn.close()
