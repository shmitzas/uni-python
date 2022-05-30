import sqlite3
import os

db_locale = os.path.dirname(__file__)+'\msdb.db'

conn = sqlite3.connect(db_locale)
c = conn.cursor()

c.execute("""
CREATE TABLE shows
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    rating TEXT NOT NULL,
    genre TEXT NOT NULL,
    seasons INTEGER NOT NULL,
    episodes INTEGER NOT NULL
)
""")
c.execute("""
CREATE TABLE movies
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    rating TEXT NOT NULL,
    genre TEXT NOT NULL
)
""")

conn.commit()
conn.close()