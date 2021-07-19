from enum import Enum


class Formats(Enum):
    FB2 = 'fb2'
    EPUB = 'epub'
    MOBI = 'mobi'
    # djvu or PDF represented as direct download
    DOWNLOAD = 'download'
