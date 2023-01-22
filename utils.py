import sqlite3


def get_all(query: str):
    '''
    Запрашиваем информацию в базе данных.
    :param query: База данных записей.
    :return: Возвращает все записи и запросы из БД.
    '''
    with sqlite3.connect('netflix.db') as cur:
        cur.row_factory = sqlite3.Row

        result = []

        for item in cur.execute(query).fetchall():
            result.append(dict(item))

        return result

def get_one(query: str):
    '''
    Запрашиваем информацию в базе данных.
    :param query: База данных записей.
    :return: Возвращается один результат из БД.
    '''
    with sqlite3.connect('netflix.db') as cur:
        cur.row_factory = sqlite3.Row
        result = cur.execute(query).fetchall()

        if result is None:
            return None
        else:
            return dict(result)

def get_movie_by_genre(type_movie, release_year, listed_in):
    '''

    :param type_movie:
    :param release_year:
    :param listed_in:
    :return:
    '''
    query = f"""
    SELECT title, description FROM netflix
    WHERE "type" = '{type_movie}'
    AND release_year = {release_year}
    AND listed_in = '%{listed_in}%'
    """

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'description': item['description']
            }
        )

    return result

def search_by_cast(name1: str = 'Jack Black', name2: str = 'Dustin Hoffman'):
    '''
    Объявляем поиск выбранных имен из БД.
    :param name1: Выбранное имя 1 Jack Black.
    :param name2: Выбранное имя 2 Dustin Hoffman
    :return: Возвращаем имена 1 и 2 из списка БД.
    '''
    query = f"""
    SELECT * FROM netflix
    WHERE netflix."cast" like '%Jack Black%' and netflix."cast" like '%Dustin Hoffman%'
    """

    cast = []
    set_cast = set()
    result = get_all(query)

    for item in result:
        for actor in item['cast'].split(','):
            cast.append(actor)

    for actor in cast:
        if cast.count(actor) > 2:
            set_cast.add(actor)

    return list(set_cast)
