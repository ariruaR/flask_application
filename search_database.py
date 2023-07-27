import sqlite3 as sql 

def get_connection_database():
  db = sql.connect('database.db')
  db.row_factory = sql.Row
  return db