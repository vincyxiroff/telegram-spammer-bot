from typing import Dict, Tuple


import os

from typing import List, Tuple
import sqlite3

conn = sqlite3.connect(os.path.join('db', 'script.db'))
cursor = conn.cursor()


def insert(table : str, values : str):
    
    values = _parse_message(values)
    #print(values)
    if table == 'links':
        column = 'link'
    else:
        column = 'message_text'

    placeholders = ', '.join('?' * len(values))
    #print (placeholders)
    cursor.executemany(
        f"INSERT INTO {table} ({column}) "
        f"VALUES ({placeholders})", [values])
    conn.commit()

def update(table : str, values : str):

    values = _parse_message(values)
    if table == 'links':
        raise Exception
    else:
        column = 'message_text'

    cursor.execute(
        f"UPDATE {table} "
        f"SET {column} = ? "
        f"WHERE id=1", values)


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
    _init_db()
    # cursor.execute("SELECT name FROM sqlite_master "
    #                 "WHERE type='table' AND name='messages'")
    # tables = cursor.fetchall()
    # print (tables)
    # if len(tables):
    #     _init_db()


def _parse_message(message : str) -> Tuple:
    parsed_msg = tuple(message.split('\n'))
    print(parsed_msg)
    return parsed_msg


check_db()
