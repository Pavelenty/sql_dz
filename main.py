from flask import Flask, request, render_template
import sqlite3 as sql
from utils import query_bd

app = Flask(__name__)

@app.route('/')
def index():
    columns_bd = ['show_id', 'title', 'country', 'release_year', 'listed_in', 'description']
    films_bd = query_bd(columns_bd, 'release_year >= 2020', 100)
    """
    Дальнейшую часть кода я хотел сделать функцией
    но в голову не пришла годная идея как это хорошо сделать, 
    поэтому оставил так
    """
    films_dict = {}
    for row in films_bd:
        films_dict[row[0]] = {
            'title': row[1],
            'country': row[2],
            'release': row[3],
            'genre': row[4],
            'description': row[5]
        }
    return render_template('index.html', search=films_dict)

@app.route('/Advanced_Search', methods=["GET", "POST"])
def Advanced_Search():
    columns_bd = ['title', 'country']
    filter = []
    post_list = ['name_film', 'country_film']
    for post_req in post_list:
        if request.form.get(post_req) != '':
            if post_req == 'name_film':
                filter.append(f'title LIKE "{request.form.get(post_req)}%"')
            if post_req == 'country':
                filter.append(f'country == "{request.form.get(post_req)}"')
    print(filter)
    films_search = query_bd(columns_bd, filter, 100)
    for row in films_search:
        print(row)
    return render_template('Advanced_Search.html')


@app.route('/DZ', methods=["GET", "POST"])
def DZ():
    return render_template('DZ.html')


if __name__ == '__main__':
    app.run(debug=True)