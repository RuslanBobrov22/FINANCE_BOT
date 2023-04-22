import sqlite3
from data_bd import data_get


def create(args):
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    for i in args:
        cur.execute(f'''ALTER TABLE purchase ADD COLUMN {i} INTEGER''')
    db.commit()
    db.close()


def add_value(desc, value):
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    cur.execute(f'''INSERT INTO purchase ({desc}, data) VALUES ({value}, {data_get()});''')
    db.commit()
    db.close()


def choose_column(col):
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    cur.execute(f"SELECT {col} FROM purchase")
    res = [i[0] for i in cur.fetchall() if i[0] is not None]
    return sum(res)


def max_column(col):
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    cur.execute(f"SELECT {col} FROM purchase")
    res = [i[0] for i in cur.fetchall() if i[0] is not None]
    return max(res)


def min_column(col):
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    cur.execute(f"SELECT {col} FROM purchase")
    res = [i[0] for i in cur.fetchall() if i[0] is not None]
    return min(res)


def store():
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    cur.execute(f"SELECT store FROM purchase")
    res = [i[0] for i in cur.fetchall() if i[0] is not None]
    return res[-1]


def store_add(value):
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    cur.execute(f'''INSERT INTO purchase (store) VALUES ({value});''')
    db.commit()
    db.close()


def store_less(value):
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    cur.execute(f'''INSERT INTO purchase (store) VALUES ({abs(value - store())});''')
    db.commit()
    db.close()


def data_filter(da):
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    da = ''.join(da.split('.'))
    cur.execute(f"SELECT * FROM purchase WHERE data == {da}")
    result = []
    for i in cur.fetchall():
        for j in i:
            if j is not None and type(j) == int:
                result.append(j)
    return sum(result)


def data_count(da):
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    da = ''.join(da.split('.'))
    cur.execute(f"SELECT * FROM purchase WHERE data == {da}")
    result = []
    for i in cur.fetchall():
        for j in i:
            if j is not None and type(j) == int:
                result.append(j)
    return len(result)


def count_column(col):
    db = sqlite3.connect('finance.db')
    cur = db.cursor()
    cur.execute(f"SELECT {col} FROM purchase")
    res = [i[0] for i in cur.fetchall() if i[0] is not None]
    return len(res)