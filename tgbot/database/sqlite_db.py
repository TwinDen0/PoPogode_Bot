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
                'city TEXT,'
                'lat   REAL,'
                'lon   REAL'
                ');')

    base.commit()

def create_user(id, login, name, city, coords):
    base = sq.connect('local.db')
    cur = base.cursor()

    sql = """ INSERT INTO users (id, login, name, city, lat, lon) VALUES (?, ?, ?, ?, ?, ?)
              ON CONFLICT (id) DO UPDATE SET city = ?, lat = ?, lon = ? """
    cur.execute(sql, (id, login, name, city, coords[0], coords[1], city, coords[0], coords[1]))

    base.commit()
    base.close()

def get_coord_db(id):
    base = sq.connect('local.db')
    cur = base.cursor()

    sql = "SELECT lat, lon FROM users WHERE id=?"
    cur.execute(sql, (id,))
    coord = cur.fetchone()

    base.commit()
    base.close()
    return coord


def get_city_sql(id):
    base = sq.connect('local.db')
    cur = base.cursor()

    sql = "SELECT city FROM users WHERE id=?"
    cur.execute(sql, (id,))
    city = cur.fetchone()[0]

    base.commit()
    base.close()
    return city