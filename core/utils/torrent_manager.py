from py1337x import Py1337x
from py1337x.types import category as py1337x_category
from py1337x.types import sort as py1337x_sort
from py1337x.models import TorrentResult, TorrentInfo


class TorrentManager:
    def __init__(self):
        self.__torrents: Py1337x | None = None

    def initialize(self):
        self.__torrents = Py1337x()

    # region apis

    def info(self, opts: dict[str, ...]) -> TorrentInfo:
        info = self.__torrents.info(
            torrent_id=opts.get("torrent_id", None),
            link=opts.get("link", None),
        )
        return info

    def search(self, opts: dict[str, ...]) -> TorrentResult:
        results = self.__torrents.search(
            query=opts.get("query", ""),
            page=opts.get("page", 1),
            category=opts.get("category", py1337x_category.TV),
            sort_by=opts.get("sort_by", py1337x_sort.SEEDERS), # type:ignore
            order=opts.get("order", "desc"), # type:ignore
        )
        return results

    def trending(self):
        return self.__torrents.trending()

    # endregion


TORRENT_MANAGER = TorrentManager()