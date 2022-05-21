import sys
from flask import Flask, render_template, request, redirect, url_for
import os
import re
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_locale = os.path.dirname(__file__)+'\db\msdb.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_locale
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.Integer)
    rating = db.Column(db.String)
    genre = db.Column(db.String)


class Shows(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.Integer)
    rating = db.Column(db.String)
    genre = db.Column(db.String)
    seasons = db.Column(db.Integer)
    episodes = db.Column(db.Integer)


@app.route('/', methods=['GET', 'POST'])
def index():
    movies, shows = getData()

    if request.method == 'POST':
        if request.form['action'] == 'update':
            try:
                data = {
                'id': request.form['id'],
                'title': request.form['title'],
                'year': request.form['year'],
                'rating': request.form['rating'],
                'genre': request.form['genre']
                }
                if request.form['category'] == 'show':
                    data['seasons'] = request.form['seasons']
                    data['episodes'] = request.form['episodes']
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

            updateItem(data, request.form['category'])
            return redirect(url_for('index'))
        elif request.form['action'] == 'add':
            try:
                data = {
                    'title': request.form['title'],
                    'year': request.form['year'],
                    'rating': request.form['rating'],
                    'genre': request.form['genre']
                }
                if request.form['category'] == 'show':
                    data['seasons'] = request.form['seasons']
                    data['episodes'] = request.form['episodes']
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

            addItem(data, request.form['category'])
            return redirect(url_for('index'))
        elif request.form['action'] == 'remove':
            removeItem(request.form['id'], request.form['category'])
            return redirect(url_for('index'))
        elif request.form['action'] == 'search':
            movies_q, shows_q = fromSearch(request.form['search'])
            print(movies_q, shows_q)
            return render_template('index.html', movies=movies_q, shows=shows_q)
        else:
            return redirect(url_for('index'))
    else:
        redirect(url_for('index'))
        return render_template('index.html', movies=movies, shows=shows)


@app.route('/edit/<req_id>', methods=['GET', 'POST'])
def edit(req_id):
    if request.method == 'POST':
        cat = request.form['category']
        if cat != None and cat == 'movie':
            data = refactorItem(Movies.query.filter_by(id=req_id).first())
            return render_template('edit.html', data=data)
        elif cat != None and cat == 'show':
            data = refactorItem(Shows.query.filter_by(id=req_id).first())
            return render_template('edit.html', data=data, category='show')
    else:
        return redirect(url_for('index'))


def getData():
    get_movies = Movies.query.filter().all()
    get_shows = Shows.query.filter().all()
    movies, shows = refactorGET(get_movies, get_shows)
    return movies, shows


def refactorGET(movies, shows):
    for item in movies:
        genre_list = re.findall(r"'(.*?)'", item.genre)
        genre = ''
        for string in genre_list:
            genre += string + ', '
        genre = genre[:-2]
        item.genre = genre

    for item in shows:
        genre_list = re.findall(r"'(.*?)'", item.genre)
        genre = ''
        for string in genre_list:
            genre += string + ', '
        genre = genre[:-2]
        item.genre = genre
    return movies, shows


def refactorItem(data):
    genre_list = re.findall(r"'(.*?)'", data.genre)
    genre = ''
    for string in genre_list:
        genre += string + ', '
    genre = genre[:-2]
    data.genre = genre
    return data


def fromSearch(search):
    search = '%{}%'.format(search)
    try:
        get_movies = Movies.query.filter(Movies.title.like(search)).all()
        get_shows = Shows.query.filter(Shows.title.like(search)).all()
        movies, shows = refactorGET(get_movies, get_shows)
        return movies, shows
    except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


def addItem(data, category):
    genres = []
    genres_split = data['genre'].split(', ')
    for item in genres_split:
        genres.append(item)
    data['genre'] = genres

    if category == 'show':
        show = Shows()
        show.title = str(data['title'])
        show.year = int(data['year'])
        show.rating = str(data['rating'])
        show.genre = str(genres)
        show.seasons = int(data['seasons'])
        show.episodes = int(data['episodes'])
        try:
            db.session.add(show)
            db.session.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    else:
        movie = Movies()
        movie.title = str(data['title'])
        movie.year = int(data['year'])
        movie.rating = str(data['rating'])
        movie.genre = str(genres)
        try:
            db.session.add(movie)
            db.session.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


def removeItem(id, category):
    print(id, category)
    if category == 'movie':
        db.session.query(Movies).filter(Movies.id == id).delete()
        db.session.commit()
    elif category == 'show':
        db.session.query(Shows).filter(Shows.id == id).delete()
        db.session.commit()


def updateItem(data, category):
    genres = []
    genres_split = data['genre'].split(', ')
    for item in genres_split:
        genres.append(item)
    data['genre'] = genres

    if category == 'show':
        show = Shows.query.filter_by(id=data['id']).first()
        show.title = str(data['title'])
        show.year = int(data['year'])
        show.rating = str(data['rating'])
        show.genre = str(genres)
        show.seasons = int(data['seasons'])
        show.episodes = int(data['episodes'])
        try:
            db.session.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    else:
        movie = Movies.query.filter_by(id=data['id']).first()
        movie.title = str(data['title'])
        movie.year = int(data['year'])
        movie.rating = str(data['rating'])
        movie.genre = str(genres)
        try:
            db.session.commit()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


if __name__ == '__main__':
    app.run(debug=True)
