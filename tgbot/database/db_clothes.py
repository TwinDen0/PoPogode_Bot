import sqlite3 as sq


def get_clothes_sql():
	base = sq.connect('local.db')
	cur = base.cursor()

	sql = """ SELECT * FROM clothes """
	clothes = cur.execute(sql).fetchone()

	base.commit()
	base.close()

	return clothes


def get_head_sql():
	base = sq.connect('local.db')
	cur = base.cursor()

	sql = """ SELECT * FROM clothes WHERE type = ?"""
	clothes = cur.execute(sql, ('голова',)).fetchall()

	base.commit()
	base.close()

	return clothes


def get_body_sql():
	base = sq.connect('local.db')
	cur = base.cursor()

	sql = """ SELECT * FROM clothes WHERE type = ?"""
	clothes = cur.execute(sql, ('тело',)).fetchall()

	base.commit()
	base.close()

	return clothes

def get_legs_sql():
	base = sq.connect('local.db')
	cur = base.cursor()

	sql = """ SELECT * FROM clothes WHERE type = ?"""
	clothes = cur.execute(sql, ('ноги',)).fetchall()

	base.commit()
	base.close()

	return clothes

def get_shoes_sql():
	base = sq.connect('local.db')
	cur = base.cursor()

	sql = """ SELECT * FROM clothes WHERE type = ?"""
	clothes = cur.execute(sql, ('ступни',)).fetchall()

	base.commit()
	base.close()

	return clothes

def get_accessories_sql():
	base = sq.connect('local.db')
	cur = base.cursor()

	sql = """ SELECT * FROM clothes WHERE type IN (?, ?, ?)"""
	clothes = cur.execute(sql, ('горло', 'руки', 'ступни_нижнее')).fetchall()

	base.commit()
	base.close()

	return clothes