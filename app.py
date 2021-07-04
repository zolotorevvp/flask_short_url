from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from hashids import Hashids

ROOT_URL = 'http://domain.com/'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://py_db_url:flask@localhost/py_db_short_url'
db = SQLAlchemy(app)


class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(2024), nullable=False)
    long_url = db.Column(db.String(1024), nullable=False)

    def __init__(self, token, long_url):
        self.token = token
        self.long_url = long_url


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def main():
    long_url = request.form.get('URL')
    try:
        check_url = requests.get(long_url).status_code
    except:
        check_url = 'Неверный URL.'
    if long_url and check_url == 200:
        hashids = Hashids(salt=long_url, min_length=6)
        token = hashids.encode(1)
        db.session.add(ShortURL(long_url, token))
        db.session.commit()
        short_url = ROOT_URL + token
        return render_template('index.html', short_URL=short_url)
    return render_template('index.html', short_URL=check_url)


if __name__ == "__main__":
    app.run(debug=1)
