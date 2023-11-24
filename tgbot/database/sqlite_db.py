import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('local.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS users ('
                'id     INTEGER UNIQUE,'
                'login  TEXT,'
                'name   TEXT,'
                'lat   REAL,'
                'lon   REAL'
                ');')

    base.commit()

def create_user(id, login, name, coords):
    base = sq.connect('local.db')
    cur = base.cursor()

    sql = """ INSERT INTO users (id, login, name, lat, lon) VALUES (?, ?, ?, ?, ?)
              ON CONFLICT (id) DO UPDATE SET lat = ?, lon = ? """
    cur.execute(sql, (id, login, name, coords[0], coords[1], coords[0], coords[1]))

    base.commit()
    base.close()

def set_coord_from_user(id):
    base = sq.connect('local.db')
    cur = base.cursor()

    sql = "SELECT lat, lon FROM users WHERE id=?"
    cur.execute(sql, (id,))
    coord = cur.fetchone()

    base.commit()
    base.close()
    return coord


