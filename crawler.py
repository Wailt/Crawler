from threading import Thread
from time import sleep

from downloader import Downloader
from page import page


class crawler(object):
    def __init__(self, init, n=3, batch=250):
        self.data = []
        self.unvisitedPage = []
        self.unvisitedPage.append(init)

        self.n = n
        self.workers = 0
        self.newSet = []

        self.batch = batch
        self.head = init
        self.bag_img = []

        self.downloader = Downloader(n=16)

    def __contains__(self, value):
        result = [i.title == value for i in self.data]
        return max(result) if result else False

    def add(self, page):
        self.data.append(page)

    def __str__(self):
        s = "Data:\n"
        for i in self.data:
            s += str(i) + "\n"
        s += "unvisited pages:\n"
        for i in self.unvisitedPage:
            s += str(i) + "\n"
        return s

    def one_hand(self, p):
        page_i = page(p, self.head)
        if p not in self:
            self.add(page_i)
        self.newSet.extend([i for i in page_i.pageList if 'http' not in i and 'irc' not in i])
        self.workers -= 1

    def to_craw(self):
        self.newSet = []
        for i in self.unvisitedPage[:self.batch]:
            while not self.has_free_hands():
                sleep(0.2)
            self.workers += 1
            Thread(target=self.one_hand, args=(i,)).start()

        while (self.workers > 0):
            sleep(0.2)

        self.newSet = list(set(self.newSet) - set([i.title for i in self.data]))
        del self.unvisitedPage[:self.batch]
        self.unvisitedPage.extend(self.newSet)

        self.newSet = []

    def has_step(self):
        return len(self.unvisitedPage) > 0

    def has_free_hands(self):
        return self.n > self.workers

    def download_img(self, method=None):
        url_img_list = []
        if not method:
            url_img_list = [i.title for i in self.data] + self.unvisitedPage
        elif method == 'visited':
            url_img_list = [i.title for i in self.data]
        elif method == 'unvisited':
            url_img_list = self.unvisitedPage

        self.downloader.download_img(url_img_list)
