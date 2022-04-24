from typing import Dict, Tuple


import os

from typing import List, Tuple
import sqlite3

conn = sqlite3.connect(os.path.join('db', 'script.db'))
cursor = conn.cursor()


def insert(table : str, values : str):
    
    #print(values)
    if table == 'links':
        column = 'link'
        values = _parse_links(values)
    else:
        column = 'message_text'

    placeholders = ', '.join('?' * len(values))
    #print (placeholders)

    for value in values:
        print(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))
        cursor.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))

    conn.commit()
        

def update(table : str, values : str):

    if table == 'links':
        column = 'link'
        values = _parse_links(values)
    else:
        column = 'message_text'

    cursor.execute(
        f"UPDATE {table} "
        f"SET {column} = ? "
        f"WHERE id=1", (values,))
    conn.commit()

def getall(table : str) -> List[str]:
    cursor.execute(f'SELECT * from {table}')
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(row[1])
    return result


def delete(table : str, values : str):
    if table == 'links':
        values = _parse_links(values)
        column = 'link'
        for value in values:
            print((value,))
            cursor.execute(f"DELETE FROM {table} where ({column}) = (?)", (value,))
    else:
        column = 'message_text'
        cursor.execute(f"DELETE FROM {table} where {column} = ?", values)
    conn.commit()

def _init_db():
    with open('createdb.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db():
    _init_db()
    # cursor.execute("SELECT name FROM sqlite_master "
    #                 "WHERE type='table' AND name='messages'")
    # tables = cursor.fetchall()
    # print (tables)
    # if len(tables):
    #     _init_db()


def _parse_links(message : str) -> Tuple:
    parsed_msg = tuple(message.split('\n'))
    print(parsed_msg)
    return parsed_msg


check_db()
