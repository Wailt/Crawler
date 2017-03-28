from urllib.request import urlopen

from threading import Thread
from time import sleep


class Downloader:
    def __init__(self, n=3):
        self.bag_img = []
        self.n = n
        self.workers = 0
        self.img = ['.img', '.jpg', '.bmp', '.png', '.svg', '.JPG', '.PNG', '.BMP', '.SVG']

    def filter_url_img(self, data):
        res = [i for i in data if max(map(lambda x: x in i, self.img)) and '/wiki/' not in i]
        print('total_images', len(res))
        return res

    def download_one_img(self, i, img):
        try:
            with urlopen('https:' + img) as url:
                s = url.read()
            out = open('images/' + str(i) + '.' + img.split('.')[-1], 'wb')
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
