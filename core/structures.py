import enum

class NavPages(enum.IntEnum):
    DASHBOARD = 0
    TORRENTS = 1
    SEARCH = 2
    SETTINGS = 3

class BrowseTableColumns(enum.IntEnum):
    NAME = 0
    SEEDERS =  1
    LEECHERS = 2
    TIME = 3
    SIZE = 4
    UPLOADER = 5

# See `https://github.com/hemantapkh/1337x/blob/main/py1337x/types/category.py`
class TorrentCategory(enum.StrEnum):
    MOVIES = 'movies'
    TV = 'tv'
    GAMES = 'games'
    MUSIC = 'music'
    APPS = 'apps'
    ANIME = 'anime'
    DOCUMENTARIES = 'documentaries'
    XXX = 'xxx'
    OTHER = 'other'