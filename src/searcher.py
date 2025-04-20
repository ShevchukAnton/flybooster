import os
import re
import time
from functools import lru_cache

import aiofiles as aiofiles
import aiohttp
from bs4 import BeautifulSoup

from enums import download_formats
from enums.download_formats import Formats
from enums.link_patterns import Pattern
from enums.search_filters import Filters

BOOSTA_URL = 'http://flibusta.is'
BASE_PAGE = f'{BOOSTA_URL}/booksearch?ask='


@lru_cache(maxsize=128, typed=False)
async def search_by_name(query=str):
    final_result = {}
    url = f'{BASE_PAGE}{query}'

    # write search result to temp file
    async with aiofiles.open(f'template-{time.time_ns()}.txt', mode='x', encoding='UTF-8') as temp:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={Filters.BOOKS.value: 'on'}) as request:
                resp = await request.text()
                await temp.write(resp)

        final_result['books'] = await parse_by_books(temp.name)

    if final_result:
        search_by_name.cache_info()
    # remove temp file at the end
    os.remove(os.path.abspath(temp.name))
    return final_result


async def search_by_author(query=str):
    final_result = {}
    url = f'{BASE_PAGE}{query}'

    # write search result to temp file
    async with aiofiles.open(f'template-{time.time_ns()}.txt', mode='x', encoding='UTF-8') as temp:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={Filters.AUTHORS.value: 'on'}) as request:
                resp = await request.text()
                await temp.write(resp)

        final_result['books'] = await parse_by_authors(temp.name)

    # remove temp file at the end
    os.remove(os.path.abspath(temp.name))
    return final_result


async def parse_by_authors(file_to_parse):
    """
    :param file_to_parse:
    :return: list of authors with params:
    books_count
    books_names
    author
    """
    authors = []
    async with aiofiles.open(file_to_parse, encoding='UTF-8') as file:
        async for line in file:
            if re.search(Pattern.BOTTOM_CUT_LINE.value, line):
                break
            parsed = BeautifulSoup(line, features="html.parser")
            links = parsed.findAll('a')
            for link in links:
                href = link.get('href')
                if re.search(Pattern.AUTHORS.value, href):
                    authors.append({'author': f'{BOOSTA_URL}{href}',
                                    'book_name': link.get_text()})
                elif re.search(Pattern.AUTHORS.value, href):
                    authors[-1][''] = link.get_text()

    return authors


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
                    if request.headers.get('Content-Disposition') and (download_formats.links[fmt.name] in request.headers.get('Content-Disposition')):
                        links[fmt.name.lower()] = url
        books_list[books_list.index(book)]['fmts'] = links

    return books_list


# TODO gather info about book
async def get_book_info(books_list):
    pass
