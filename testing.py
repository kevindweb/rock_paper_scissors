import sqlite3 as sql
db = sql.connect('./my_data.db')
cursor = db.cursor()

# cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (username text, password text)""")
# cursor.execute("""CREATE TABLE IF NOT EXISTS rps_data (username text, games_played integer, other_data text)""")

