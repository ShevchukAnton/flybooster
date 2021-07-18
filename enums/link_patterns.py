from enum import Enum


class Pattern(Enum):
    BOOKS = '/b/\d+'
    AUTHORS = '/a/\d+'
    SERIES = '/sequence/\d+'
    GENRES = '/g/.+'
    # keyword after which begin some advertisement trash
    BOTTOM_CUT_LINE = 'id="sidebar-right'
