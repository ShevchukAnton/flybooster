from enum import Enum

links = {
    'FB2': 'fb2.zip',
    'MOBI': 'fb2.mobi',
    'EPUB': 'fb2.epub',
    'PDF': '.pdf',
    'DJVU': '.djvu',
}


class Formats(Enum):
    FB2 = 'fb2'
    EPUB = 'epub'
    MOBI = 'mobi'
    # djvu or PDF represented as direct download
    PDF = 'download'
    DJVU = 'download'
