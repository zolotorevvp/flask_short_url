from html import escape
from flask_login import UserMixin

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from hashids import Hashids

ROOT_URL = 'http://127.0.0.1:5000/'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://py_db_url:flask@localhost/py_db_short_url'
db = SQLAlchemy(app)


class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(32), nullable=False)
    long_url = db.Column(db.String(2024), nullable=False)

    def __init__(self, token, long_url):
        self.token = token
        self.long_url = long_url




class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def main():
    long_url = request.form.get('URL')
    check_url = ''
    if long_url:
        try:
            check_url = requests.get(long_url).status_code
        except:
            check_url = 'Неверный URL.'
        if check_url == 200:
            hashids = Hashids(salt=long_url, min_length=6)
            token = hashids.encode(1)
            db.session.add(ShortURL(token=token, long_url=long_url))
            db.session.commit()
            short_url = ROOT_URL + token
            return render_template('index.html', short_URL=short_url)
    return render_template('index.html', short_URL=check_url)


@app.route('/<token>')
def show_subpath(token):
    print(escape(token))
    s = ShortURL.query.filter_by(token=token).first()
    print('fgfg', type(s))
    return f'Subpath {escape(token)}'


if __name__ == "__main__":
    app.run(debug=1)
