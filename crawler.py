from threading import Thread
from time import sleep, time

from downloader import Downloader
from page import page


class crawler(object):
    def __init__(self, init, n=3, batch=250):
        self.data = []
        self.unvisitedPage = {init}

        self.n = n
        self.workers = 0
        self.newSet = []

        self.batch = batch
        self.head = init

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

    def one_step(self):
        self.newSet = []
        delete = list(self.unvisitedPage)[:self.batch]
        for i in delete:
            while not self.has_free_hands():
                sleep(0.2)
            self.workers += 1

            Thread(target=self.one_hand, args=(i,)).start()

        while (self.workers > 0):
            sleep(0.2)

        self.newSet = set(self.newSet) - set([i.title for i in self.data])
        self.unvisitedPage.difference_update(delete)
        self.unvisitedPage.update(self.newSet)

        self.newSet = []

    def to_craw(self):
        n = 1
        b = time()
        while (self.has_step()):
            self.one_step()
            n += self.batch
            print('new iteration')
            print('visited', len(self.data), '\n',
                  'unvisited', len(self.unvisitedPage))
            print('mean_time:', (time() - b) / n, '\n',
                  'iter time:', (time() - b))
            print('fraction', round(len(self.unvisitedPage) / len(self.data), 1))
            print('passed', round(len(self.data) / (len(self.unvisitedPage) + len(self.data)), 2))
            print('\n')

    def has_step(self):
        return len(self.unvisitedPage) > 0

    def has_free_hands(self):
        return self.n > self.workers

    def download_img(self, method=None):
        url_img_list = []
        if not method:
            url_img_list = [i.title for i in self.data] + list(self.unvisitedPage)
        elif method == 'visited':
            url_img_list = [i.title for i in self.data]
        elif method == 'unvisited':
            url_img_list = list(self.unvisitedPage)

        self.downloader.download_img(url_img_list)
