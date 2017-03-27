import urllib
from threading import Thread
from time import sleep


class Downloader:
    def __init__(self, n=3):
        self.bag_img = []
        self.n = n
        self.workers = 0

    def filter_url_img(self, data):
        img = ['.img', '.jpg', '.bmp', '.png', '.svg']
        res = []
        for i in data:
            if max(map(lambda x: x in i, img)) and '/wiki/' not in i:
                res.append(i)
        print('total_images', len(res))
        return res

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

    def download_img(self, data):
        res = self.filter_url_img(data)
        for i, img in enumerate(res):
            while self.workers >= self.n:
                sleep(0.2)
            self.workers += 1
            Thread(target=self.download_one_img, args=(i, img)).start()
        print('uploading done!')
