from flask import Flask, request, render_template
import sqlite3 as sql
from utils import query_bd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Advanced_Search', methods=["GET", "POST"])
def Advanced_Search():
    search_get = request.form.get('test')
    print(search_get)
    return render_template('Advanced_Search.html')


@app.route('/DZ')
def DZ():
    return render_template('DZ.html')


if __name__ == '__main__':
    app.run(debug=True)