from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import re

app = Flask(__name__)
db_locale = os.path.dirname(__file__)+'\db\msdb.db'


@app.route('/', methods=['GET', 'POST'])
def index():
    movies, shows = getData()
    if request.method == 'POST':
        if request.form['action'] == 'add':
            addItem(request.form, movies, shows)
        else:
            removeItem(request.form['id'], request.form['category'], len(movies)-1, len(shows)-1)
        return redirect(url_for('index'))
    return render_template('index.html', movies=movies, shows=shows)


def getData():
    db_locale = os.path.dirname(__file__)+'\db\msdb.db'
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute('SELECT * FROM movies')
    get_movies = c.fetchall()
    c.execute('SELECT * FROM shows')
    get_shows = c.fetchall()

    conn.commit()
    conn.close()

    movies, shows = refactorGET(get_movies, get_shows)

    return movies, shows


def refactorGET(movies, shows):
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
    return proc_movies, proc_shows


def addItem(data, movies_org, shows_org):
    to_save = {}
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()

    if '' not in data.values():
        if data['category'] == 'movie':
            to_save['id'] = int(movies_org[len(movies_org)-1][0] + 1)
            to_save['title'] = str(data['title'])
            to_save['year'] = int(data['year'])
            to_save['rating'] = str(data['rating'])
            to_save['genre'] = str(list(data['genre'].split(', ')))
            c.execute('INSERT INTO movies(title, year, rating, genre) VALUES("{}", "{}", "{}", "{}")'.format(
                str(to_save['title']), int(to_save['year']), str(to_save['rating']), str(to_save['genre'])))
        elif data['category'] == 'show':
            to_save['id'] = int(shows_org[len(shows_org)-1][0] + 1)
            to_save['title'] = str(data['title'])
            to_save['year'] = int(data['year'])
            to_save['rating'] = str(data['rating'])
            to_save['genre'] = str(list(data['genre'].split(', ')))
            to_save['seasons'] = int(data['seasons'])
            to_save['episodes'] = int(data['episodes'])
            c.execute('INSERT INTO shows(title, year, rating, genre, seasons, episodes) VALUES("{}", "{}", "{}", "{}", "{}", "{}")'.format(str(
                to_save['title']), int(to_save['year']), str(to_save['rating']), str(to_save['genre']), int(to_save['seasons']), int(to_save['episodes'])))
        else:
            print('Unknown category: {}'.format(data['category']))
    else:
        print('POST is empty', data)
    conn.commit()
    conn.close()


def removeItem(id, category, movie_count, show_count):
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    if category == 'movie':
        c.execute('DELETE FROM movies WHERE id = {};'.format(id))
        c.execute('UPDATE SQLITE_SEQUENCE SET seq = {} WHERE NAME = "movies";'.format(movie_count))
    elif category == 'show':
        c.execute('DELETE FROM shows WHERE id = {};'.format(id))
        c.execute('UPDATE SQLITE_SEQUENCE SET seq = {} WHERE NAME = "shows";'.format(show_count))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)
