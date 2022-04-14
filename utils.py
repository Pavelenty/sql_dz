import sqlite3 as sql

def query_bd(name_columns, filters, limit=0, operation='AND', name_bd = 'netflix'):
    if isinstance(name_columns, list):
        name_columns_convert = ", ".join(name_columns)
    else:
        name_columns_convert = name_columns

    if isinstance(filters, list):
        filters_convert = f" {operation} ".join(filters)
    else:
        filters_convert = filters

    if limit == 0:
        q_limit = ''
    else:
        q_limit = f'LIMIT {limit}'

    query = f"""
                SELECT {name_columns_convert}
                FROM {name_bd}
                WHERE {filters_convert}
                {q_limit};
            """

    with sql.connect("data/netflix.db") as connect:
        cursor = connect.cursor()
    return cursor.execute(query)

def filtered_list(column):
    genre_list = []
    bd_column = query_bd(column, f'{column} <> ""')
    for el in bd_column:
        el_list = el[0].split(',')
        for el_el in el_list:
            el_el = el_el.replace(' ', '')
            genre_list.append(el_el)
    genre_list = set(genre_list)
    return list(genre_list)


def search_genre(genre):
    list_search_genre = []
    bd_column = query_bd('title, description', f'listed_in LIKE "{genre}%"', 10)
    for el in bd_column:
        list_search_genre.append({
            "title": el[0],
            "description": el[1]
        })
    return list_search_genre

