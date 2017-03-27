from bs4 import BeautifulSoup
from requests import get


def encode_and_replace(li):
    li.encode('UTF-8')
    return li.attrs['href'] if 'href' in li.attrs else ''


class page(object):
    def getHiperlinks(self):
        if self.title == self.head:
            url = self.head
        else:
            url = self.head + self.title

        req = get(url)
        try:
            soup = BeautifulSoup(req.content.decode(req.encoding), "lxml")
            arList = [encode_and_replace(li) for li in soup.findAll('a')]
            arList = list(set([i for i in arList if self.validation(i)]))
            return arList
        except:
            return []

    def __init__(self, title, head):
        self.title = title
        self.head = head
        self.pageList = self.getHiperlinks()

    def __str__(self):
        s = "(" + str(self.title) + ":\n  "
        for i in self.pageList:
            s += str(i) + ";  "
        s += ')'
        return s

    def validation(self, ar):
        bad = min(list(map(lambda x: not x in ar, features_not)))
        return bad


features_not = ['Special', '.wikipedia.org',
                'wikidata', 'wiktionary', 'wikibooks',
                'wikiquote', 'en.wiki',
                'wikinews', 'meta.w', 'mediawiki', '/w/']
