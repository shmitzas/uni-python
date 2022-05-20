from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
import os

app = Flask(__name__)

db_name = 'cheaper.sqlite3'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

ROWS_PER_PAGE = 5

class Product(db.Model):
    __tablename__ = 'output_moto'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price = db.Column(db.String)
    image = db.Column(db.String)
    link = db.Column(db.String)

    
@app.route('/')
def index():
    try:
        products = Product.query.all()
        return render_template('index.html', products=products)
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/')
def search():
        q = request.args.get('q')

        if q:
            page = request.args.get('page', 1, type=int)
            search = Product.query.filter(Product.title.contains(q))
            products = search.paginate(per_page=20)
        else:
            page = request.args.get('page', 1, type=int)
            products = Product.query.paginate(per_page=20)
        return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True) 