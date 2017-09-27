import urllib.request
import time
## скачать все страницы: в цикле по темам подцикле по страницам. Сохранить в отдельную папку
def getpages():
    form = 'http://www.surskieprostori.ru/news-%d-%d.html'
    for i in range(1,44):
        for j in range(1, 4585):
            req = urllib.request.Request(form%(i,j))
            with urllib.request.urlopen(req) as response:
                    html = response.read().decode('utf-8')
                    time.sleep(1)
                    ##Здесь надо, чтобы из каждого файла на этом месте извлекалась нужная инфа и отсекалось лишнее
                    ##Сортировка по каталогам

def processing(page):
    ##нужно: дата, чтобы сортировать - год, месяц
