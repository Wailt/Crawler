import urllib
from threading import Thread
from time import sleep
from time import time

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
        self.newSet += [i for i in page_i.pageList if 'http' not in i and 'irc' not in i]
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

    def filter_url_img(self, uns=False):
        img = ['.img', '.jpg', '.bmp', '.png', '.svg']
        res = []
        if not uns:
            for i in self.data:
                if max(map(lambda x: x in i.title, img)) and '/wiki/' not in i.title:
                    res.append(i.title)
            return res
        else:
            return self.unvisitedPage

    def download_one_img(self, i, img):
        try:
            with urllib.request.urlopen('https:' + img) as url:
                s = url.read()
            t = img.split('.')[-1]
            out = open('images/' + str(i) + '.' + t, 'wb')
            out.write(s)
            out.close()
            self.workers -= 1
        except:
            self.bag_img.append(img)
            self.workers -= 1

    def download_img(self, uns=False):
        res = self.filter_url_img(uns=uns)
        for i, img in enumerate(res):
            while (self.workers >= self.n):
                sleep(0.2)
            self.workers += 1
            Thread(target=self.download_one_img, args=(i, img)).start()
        print('uploading done!')
