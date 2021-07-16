import os
import re

import requests

BASE_PAGE = 'http://flibusta.is/booksearch?ask='
SERIES_FILTER = 'chs'
AUTHORS_FILTER = 'cha'
BOOKS_FILTER = 'chb'
GENRES_FILTER = 'chg'

ALL_FILTERS = {
    # Series
    SERIES_FILTER: 'on',
    # Authors
    AUTHORS_FILTER: 'on',
    # Books
    BOOKS_FILTER: 'on',
    # Genres
    GENRES_FILTER: 'on'
}

# keyword after which begin some advertisement trash
BOTTOM_CUT_LINE = 'id="sidebar-right'

BOOKS_LINK_PATTERN = '/b/\d+'
AUTHORS_LINK_PATTERN = '/a/\d+'
SERIES_LINK_PATTERN = '/sequence/\d+'
GENRES_LINK_PATTERN = '/g/.+'


def find(query=str, filters=ALL_FILTERS):
    final_result = {}
    # &{"&".join(filters)}
    url = f'{BASE_PAGE}{query}'

    # write search result to temp file
    with(open('template.txt', 'w', encoding='UTF-8')) as temp:
        temp.write(requests.get(url, filters).text)

    # TODO maybe change this part to something better instead storing all in one place
    if filters[BOOKS_FILTER]:
        final_result['books'] = parse_by_books(temp.name)
    elif filters[AUTHORS_FILTER]:
        final_result['authors'] = parse_by_authors(temp.name)
    elif filters[GENRES_FILTER]:
        final_result['genres'] = parse_by_genres(temp.name)
    elif filters[SERIES_FILTER]:
        final_result['series'] = parse_by_series(temp.name)

    # remove temp file at the end
    os.remove(os.path.abspath(temp.name))
    return final_result


# TODO
def parse_by_authors(file_to_parse):
    pass


# TODO
def parse_by_series(file_to_parse):
    pass


# TODO
def parse_by_genres(file_to_parse):
    pass


# TODO add sanitizing
def parse_by_books(file_to_parse):
    books = []
    with(open(file_to_parse, 'r', encoding='UTF-8')) as file:
        for line in file:
            if re.search(BOOKS_LINK_PATTERN, line):
                books.append(line)
            elif re.search(BOTTOM_CUT_LINE, line):
                break

    return books


# TODO
def sanitize_html(text_to_sanitize):
    pass
