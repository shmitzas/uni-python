from flask import Flask, render_template, request
import sqlite3
import os
import re

app = Flask(__name__)


@app.route('/')
def index():
    movies, shows = getData()
    proc_movies = []
    proc_shows = []
    for item in movies:
        genre_list = re.findall(r"'(.*?)'", item[4])
        genre = ''
        for string in genre_list:
            genre += string + ', '
        genre = genre[:-2]
        tmp_list = []
        tmp_list.append(item[0])
        tmp_list.append(item[1])
        tmp_list.append(item[2])
        tmp_list.append(item[3])
        tmp_list.append(genre)
        proc_movies.append(tmp_list)

    for item in shows:
        genre_list = re.findall(r"'(.*?)'", item[4])
        genre = ''
        for string in genre_list:
            genre += string + ', '
        genre = genre[:-2]
        tmp_list = []
        tmp_list.append(item[0])
        tmp_list.append(item[1])
        tmp_list.append(item[2])
        tmp_list.append(item[3])
        tmp_list.append(genre)
        tmp_list.append(item[5])
        tmp_list.append(item[6])
        proc_shows.append(tmp_list)

    test_t = 'testinis tekstas bbz ar paeis'
    return render_template('index.html', movies=proc_movies, shows=proc_shows, test_t=test_t)


def getData():
    db_locale = os.path.dirname(__file__)+'\db\msdb.db'
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute('SELECT * FROM movies')
    movies = c.fetchall()
    c.execute('SELECT * FROM shows')
    shows = c.fetchall()

    conn.commit()
    conn.close()

    return movies, shows


def addItem():
    pass


def removeItem():
    pass


if __name__ == '__main__':
    app.run(debug=True)
# task4\db\msdb.db
# task4\main.py
