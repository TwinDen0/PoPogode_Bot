import sqlite3 as sq


def get_clothes_sql():
	base = sq.connect('local.db')
	cur = base.cursor()

	sql = """ SELECT * FROM clothes """
	clothes = cur.execute(sql).fetchone()
	print(clothes)

	base.commit()
	base.close()

	return clothes


def get_head_sql():
	base = sq.connect('local.db')
	cur = base.cursor()

	sql = """ SELECT * FROM clothes WHERE type = ?"""
	clothes = cur.execute(sql, ('голова',)).fetchall()
	print(clothes)

	base.commit()
	base.close()

	return clothes


def get_body_sql():
	base = sq.connect('local.db')
	cur = base.cursor()

	sql = """ SELECT * FROM clothes WHERE type = ?"""
	clothes = cur.execute(sql, ('тело',)).fetchall()
	print(clothes)

	base.commit()
	base.close()

	return clothes

