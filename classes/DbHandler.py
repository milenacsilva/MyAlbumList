#!/usr/bin/env python3

import psycopg2
from typing import List
from dotenv import dotenv_values
import os
import sys
from classes import Interface


class DbHandler():
    _instance = None
    running = False

    def __init__(self):
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
            self.cur = self.conn.cursor()
            self.running = True
        except Exception as e:
            Interface.Interface.instance().kill()
            print("Erro na conexão com o banco de dados!")
            print(f"Erro de conexão com o DB: {e}", file=sys.stderr)

    def fetchOne(self, query: str, params: List[str]):
        self.cur.execute(query, params)
        return self.cur.fetchone()

    def fetchAll(self, query: str, params: List[str]):
        self.cur.execute(query, params)
        return self.cur.fetchall()

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
