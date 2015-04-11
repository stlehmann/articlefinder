from PyQt5.QtCore import QThread, pyqtSignal


class WorkerThread(QThread):
    """
    Thread for doing all the work:
        * finding the articles in the shops
        * downloading images

    """
    progress = pyqtSignal(int, int, str, name="progress")

    def __init__(self):
        super(WorkerThread, self).__init__()
        self._cancel = False
        self.shops = []
        self.search_term = ""
        self.articles = []

    def run(self):
        def _find():
            for i, shop in enumerate(self.shops):
                self.progress.emit(i, len(self.shops),
                                   "Suche Artikel bei %s" % shop.name)
                for a in shop.find(self.search_term):
                    yield a
                    if self._cancel:
                        return

        self._cancel = False
        self.articles = list(_find())
        self._cancel = False
        for i, article in enumerate(self.articles):
            if self._cancel:
                return
            self.progress.emit(i, len(self.articles), "Bilder herunterladen")
            article.image = article.shop.download_image(article.image_url)

    def quit(self):
        self._cancel = True