import os
import re

import requests

from enums.link_patterns import Pattern
from enums.search_filters import Filters

BASE_PAGE = 'http://flibusta.is/booksearch?ask='

ALL_FILTERS = {
    # Series
    Filters.SERIES: 'on',
    # Authors
    Filters.AUTHORS: 'on',
    # Books
    Filters.BOOKS: 'on',
    # Genres
    Filters.GENRES: 'on'
}


def find(query=str, filters=ALL_FILTERS):
    final_result = {}
    url = f'{BASE_PAGE}{query}'

    # write search result to temp file
    with(open('/tmp/template.txt', 'w', encoding='UTF-8')) as temp:
        temp.write(requests.get(url, filters).text)

    # TODO maybe change this part to something better instead storing all in one place
    if filters[Filters.BOOKS]:
        final_result['books'] = parse_by_books(temp.name)
    elif filters[Filters.AUTHORS]:
        final_result['authors'] = parse_by_authors(temp.name)
    elif filters[Filters.GENRES]:
        final_result['genres'] = parse_by_genres(temp.name)
    elif filters[Filters.GENRES]:
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
            if re.search(Pattern.BOOKS, line):
                books.append(line)
            elif re.search(Pattern.BOTTOM_CUT_LINE, line):
                break

    return books


# TODO
def sanitize_html(text_to_sanitize):
    pass
