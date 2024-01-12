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
                'lon   REAL,'
                'clock   TEXT'
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

def check_user_exists(user_id):
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    if cur.fetchone():
        return True
    else:
        return False

def check_reminder_exists(user_id):
    cur.execute("SELECT clock FROM users WHERE id=?", (user_id,))
    if cur.fetchone()[0] != None:
        return True
    else:
        return False

def set_user_clock_reminder(clock, user_id):
    cur.execute("UPDATE users SET clock=? WHERE id=?", (clock, user_id,))
    base.commit()

def del_reminder(user_id):
    cur.execute("UPDATE users SET clock=NULL WHERE id=?", (user_id,))
    base.commit()

def get_all_users():
    users = []
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for row in rows:
        user = {
            "id": row[0],
            "login": row[1],
            "name": row[2],
            "city": row[3],
            "lat": row[4],
            "lon": row[5]
        }
        users.append(user)
    return users

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