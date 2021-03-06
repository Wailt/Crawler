from bs4 import BeautifulSoup
from requests import get


def encode_and_replace(li):
    li.encode('UTF-8')
    return li.attrs['href'] if 'href' in li.attrs else ''


class page(object):
    def __getHiperlinks(self):
        url = self.head if self.title == self.head else self.head + self.title
        try:
            req = get(url)
            soup = BeautifulSoup(req.content.decode(req.encoding), "lxml")
            ar_list = [encode_and_replace(li) for li in soup.findAll('a')]
            return list(set([i for i in ar_list if self.__valid(i)]))

        except:
            return []

    def __init__(self, title, head):
        self.title = title
        self.head = head
        self.pageList = self.__getHiperlinks()

    def __str__(self):
        s = "(" + str(self.title) + ":\n  "
        for i in self.pageList:
            s += str(i) + ";  "
        s += ')'
        return s

    def __valid(self, ar):
        bad = min(list(map(lambda x: not x in ar, features_not)))
        return bad


features_not = ['Special', '.wikipedia.org',
                'wikidata', 'wiktionary', 'wikibooks',
                'wikiquote', 'en.wiki',
                'wikinews', 'meta.w', 'mediawiki', '/w/']
