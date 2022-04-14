from flask import Flask, request, render_template
import sqlite3 as sql
from utils import query_bd, filtered_list, search_genre

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
    columns_bd = ['show_id', 'title', 'country', 'listed_in', 'rating', 'release_year', 'description']
    filter = []
    post_list = ['name_film', 'country_film', 'genre', 'rating', 'release_year_one', 'release_year_two']
    genre_list = filtered_list('listed_in')
    genre_list = ['Любой'] + genre_list
    for post_req in post_list:
        if request.form.get(post_req) != '' and request.form.get(post_req) != 'Любой':
            if post_req == 'name_film':
                filter.append(f'title LIKE "{request.form.get(post_req)}%"')
            if post_req == 'country':
                filter.append(f'country == "{request.form.get(post_req)}"')
            if post_req == 'genre':
                filter.append(f'listed_in LIKE "{request.form.get(post_req)}%"')
            if post_req == 'rating':
                filter.append(f'rating == "{request.form.get(post_req)}"')
            if post_req == 'release_year_one':
                filter.append(f'release_year >= "{request.form.get(post_req)}"')
            if post_req == 'release_year_two':
                filter.append(f'release_year <= "{request.form.get(post_req)}"')
    films_search = query_bd(columns_bd, filter, 100)

    films_dict = {}
    for row in films_search:
        films_dict[row[0]] = {
            'title': row[1],
            'country': row[2],
            'release': row[5],
            'genre': row[3],
            'rating': row[4],
            'description': row[6]
        }
    return render_template('Advanced_Search.html', genre_list=genre_list, search=films_dict)


@app.route('/movie/<title>', methods=["GET", "POST"])
@app.route('/movie', methods=["GET", "POST"])
def DZ(title='d'):
    name = request.form.get('name_film')
    columns_bd = ['show_id', 'title', 'country', 'release_year', 'listed_in', 'description']
    films_bd = query_bd(columns_bd, f'title LIKE "{title}%"', 100)
    films_dict = {}
    for row in films_bd:
        films_dict[row[0]] = {
            'title': row[1],
            'country': row[2],
            'release': row[3],
            'genre': row[4],
            'description': row[5]
        }
    return render_template('DZ.html', search=films_dict, name=name)


@app.route('/rating/<rat>', methods=["GET", "POST"])
def rating(rat):
    rating_list = []
    if rat == 'children':
        rating_list = ['G']
    if rat == 'family':
        rating_list = ['G', 'PG', 'PG-13']
    if rat == 'adult':
        rating_list = ['R', 'NC-17']
    filter = []
    for rating in rating_list:
        filter.append(f'rating == "{rating}"')
    columns_bd = ['show_id', 'title', 'country', 'release_year', 'listed_in', 'description']
    films_bd = query_bd(columns_bd, filter, 100, 'OR')

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


@app.route('/genre/<genre>')
def genre_search(genre):
    desired_element = search_genre(genre)
    return render_template('genre.html', list=desired_element)

if __name__ == '__main__':
    app.run(debug=True)