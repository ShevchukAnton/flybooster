import os
import re
import time

import aiofiles as aiofiles
import aiohttp
from bs4 import BeautifulSoup

from enums import download_formats
from enums.download_formats import Formats
from enums.link_patterns import Pattern
from enums.search_filters import Filters

BOOSTA_URL = 'http://flibusta.is'
BASE_PAGE = f'{BOOSTA_URL}/booksearch?ask='

DEFAULT_FILTERS = {
    Filters.BOOKS.value: 'on'
}


async def find(query=str, filters=DEFAULT_FILTERS):
    final_result = {}
    url = f'{BASE_PAGE}{query}'

    # write search result to temp file
    async with aiofiles.open(f'template-{time.time_ns()}.txt', mode='x', encoding='UTF-8') as temp:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=filters) as request:
                resp = await request.text()
                await temp.write(resp)
        # TODO maybe change this part to something better instead storing all in one place
        if filters[Filters.BOOKS.value]:
            final_result['books'] = await parse_by_books(temp.name)
        elif filters[Filters.AUTHORS.value]:
            final_result['authors'] = await parse_by_authors(temp.name)
        elif filters[Filters.GENRES.value]:
            final_result['genres'] = await parse_by_genres(temp.name)
        elif filters[Filters.GENRES.value]:
            final_result['series'] = await parse_by_series(temp.name)

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
async def parse_by_books(file_to_parse):
    """
    :param file_to_parse:
    :return: list of books with params:
    book_link
    book_name
    author
    fmts
    """
    books = []
    async with aiofiles.open(file_to_parse, encoding='UTF-8') as file:
        async for line in file:
            if re.search(Pattern.BOTTOM_CUT_LINE.value, line):
                break
            parsed = BeautifulSoup(line, features="html.parser")
            links = parsed.findAll('a')
            for link in links:
                href = link.get('href')
                if re.search(Pattern.BOOKS.value, href):
                    books.append({'book_link': f'{BOOSTA_URL}{href}',
                                  'book_name': link.get_text()})
                elif re.search(Pattern.AUTHORS.value, href):
                    books[-1]['author'] = link.get_text()

    books = await find_downloadable_formats(books)
    return books


# TODO check which formats available for download
async def find_downloadable_formats(books_list):
    for book in books_list:
        link = book.get('book_link')
        links = {}
        for fmt in Formats:
            url = f'{link}/{fmt.value}'
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as request:
                    if request.headers.get('Content-Disposition').__contains__(download_formats.links[fmt.name]):
                        links[fmt.name.lower()] = url
        books_list[books_list.index(book)]['fmts'] = links

    return books_list


# TODO gather info about book
async def get_book_info(books_list):
    pass
