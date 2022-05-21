import sqlite3
import json
import os

movies = []
shows = []
filename = (os.path.dirname(__file__)) + '/data.json'
try:
    if os.stat(filename).st_size > 0:
        with open(filename, encoding="utf-8") as file:
            from_json = json.load(file)
            for item in from_json:
                if item['category'] == 'movie':
                    # movie = (item['title'], item['year'], item['rating'], item['genre'])
                    movies.append(item)
                elif item['category'] == 'tv-show':
                    # show = (item['title'], item['year'], item['rating'], item['genre'], item['seasons'], item['episodes'])
                    shows.append(item)
                else:
                    print("Some item is neither a movie, nor a tv show!")
    else:
        print('File "data.json" is empty!')
        exit()
except OSError:
    print('File "data.json" does not exist!')
    exit()
except KeyError:
    print('Some item in "data.json" is empty or missing an attribute!')
    exit()

db_locale = os.path.dirname(__file__)+'\msdb.db'

def checkData():
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()
    c.execute('SELECT * FROM movies')
    movies = c.fetchall()
    print('\n----- Movies -----\n', movies)
    c.execute('SELECT * FROM shows')
    shows = c.fetchall()
    print('\n----- Shows -----\n', shows)

    conn.commit()
    conn.close()

def insertData():
    conn = sqlite3.connect(db_locale)
    c = conn.cursor()

    for item in shows:
        c.execute('INSERT INTO shows(title, year, rating, genre, seasons, episodes) VALUES("{}", "{}", "{}", "{}", "{}", "{}")'.format(str(
            item['title']), int(item['year']), str(item['rating']), str(item['genre']), int(item['seasons']), int(item['episodes'])))

    for item in movies:
        c.execute('INSERT INTO movies(title, year, rating, genre) VALUES("{}", "{}", "{}", "{}")'.format(
            str(item['title']), int(item['year']), str(item['rating']), str(item['genre'])))

    conn.commit()
    conn.close()

insertData()