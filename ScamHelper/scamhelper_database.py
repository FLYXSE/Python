import sqlite3

from time import sleep

import datetime


# Регистрация пользователя

def user_exists_database(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			return bool(len(result))
	except:
		return False

def user_add_database(user_id, username):
	try:
		date = datetime.date.today()
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO `users` (`user_id`, `username`, `date`, `warning`) VALUES(?,?,?,?)", (user_id, username, date, 0))
	except Exception as e:
		print(e)



# Получение значений

def user_username(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[1]
	except:
		pass


def user_warning(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[3]
	except:
		pass

def user_date(user_id):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			result = cur.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
			for row in result:
				return row[2]
	except:
		pass		


def users_db():
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute('SELECT count(*) FROM `users`').fetchall()[0]
			rows = list(rows)
			return rows[0]
	except:
		pass		

def user_id_db():
	try:
		array = []
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			rows = cur.execute('SELECT * FROM `users`').fetchall()
			for row in rows:
				array.append(row[0])

		return array
	except:
		pass

# Обновление значений

def user_update_username(user_id, username):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `username` = ? WHERE `user_id` = ?", (username, user_id))
	except:
		pass


def user_update_warning(user_id, warning):
	try:
		with sqlite3.connect("evidence.db") as con:
			cur = con.cursor()
			cur.execute("UPDATE `users` SET `warning` = warning + ? WHERE `user_id` = ?", (warning, user_id))
	except:
		pass				