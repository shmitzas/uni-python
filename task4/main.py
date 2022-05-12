from flask import Flask, render_template, request
import sqlite3
import os


app = Flask(__name__)


@app.route('/')
def index():
    movies, shows = getData()
    test_t = 'testinis tekstas bbz ar paeis'
    return render_template('index.html', movies=movies, shows=shows, test_t=test_t)


def getData():
    db_locale = os.path.dirname(__file__)+'\db\msdb.db'
    print('\n\n\n',os.stat(db_locale).st_size,'\n', db_locale, '\n\n\n')
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

    return movies, shows

if __name__ == '__main__':
    app.run(debug=True)
# task4\db\msdb.db
# task4\main.py