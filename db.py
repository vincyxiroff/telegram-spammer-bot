from msilib.sequence import tables
from typing import Dict


import os

from typing import List, Tuple
import sqlite3

conn = sqlite3.connect(os.path.join('db', 'script.db'))
cursor = conn.cursor()


def insert(table : str, values : Tuple):
    if table == 'links':
        column = 'link'
    else:
        column = 'message_text'

    placeholders = ', '.join('?' * len(values))
    cursor.executemany(
        f'INSERT INTO {table} {column}'
        f'VALUES ({placeholders})', values)
    conn.commit()



def getall(table : str) -> List[str]:
    cursor.execute(f'SELECT * from {table}')
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row[1])
    return result


def delete(table : str, row_id : int):
    row_id = int(row_id)
    cursor.execute(f'DELETE FROM {table} WHERE id={row_id}')
    conn.commit()


def _init_db():
    with open('createdb.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit


def check_db():
    cursor.execute("SELECT name FROM sqlite_master "
                    "WHERE type='table' AND (name='lnks' OR name='messages')")
    tables = cursor.fetchall()
    if len(tables) < 2:
        _init_db()


check_db()
