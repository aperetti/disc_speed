import sqlite3
from time import time
from datetime import datetime

LATEST_VERSION = 2.1

def init_db(con: sqlite3.Connection):
    con.execute("DROP TABLE IF EXISTS throws")
    con.execute("""
        CREATE TABLE IF NOT EXISTS throws (
            id integer primary key autoincrement
            , dt text
            , speed numeric)
        """)
    con.execute("INSERT INTO version VALUES (1, ?) ON CONFLICT(id) DO UPDATE SET version = ?", (LATEST_VERSION, LATEST_VERSION))
    con.commit()

def connect_db():
    con = sqlite3.connect(".db")
    con.execute("CREATE TABLE IF NOT EXISTS version (id integer primary key autoincrement, version numeric)")
    version = con.execute("SELECT version FROM version WHERE id = 1").fetchone()
    if version is None or version[0] is not LATEST_VERSION:
        init_db(con)
    return con

def save_throw(con, speed):
    con.execute("INSERT INTO throws(dt, speed) VALUES (datetime('now'),?)", (speed,))
    con.commit()

if __name__ == "__main__":
    con = connect_db()
    save_throw(con, 60)