from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from hashids import Hashids


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://flask_url:flask@localhost/db_shortening'
db = SQLAlchemy(app)




class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), nullable=False)
    long_url = db.Column(db.String(1024), nullable=False)


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/add_url', methods=['GET', 'POST'])
def add_url():
    url = request.form['URL']
    hashids = Hashids(salt=url, min_length=8)
    token = hashids.encode(1)
    return render_template('index.html', short_URL=token)


if __name__ == "__main__":
    app.run(debug=1)
