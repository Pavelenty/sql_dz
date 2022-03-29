import sqlite3 as sql

def query_bd(name_columns, filters, limit=0, name_bd = 'netflix'):
    if isinstance(name_columns, list):
        name_columns_convert = ", ".join(name_columns)
    else:
        name_columns_convert = name_columns

    if isinstance(filters, list):
        filters_convert = " AND ".join(filters)
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