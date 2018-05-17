## Умеет выкачивать все новости с сайта сурских просторов, парсить их, а потом стеммить майстемом в двух вариантах - просто так и в xml.

import urllib.request
import re
import os
import html

##Функции обработки текста

def clean(t):
    regTag = re.compile('<.*?>', re.DOTALL)  # это рег. выражение находит все тэги
    regScript = re.compile('<script>.*?</script>', re.DOTALL) # все скрипты
    regComment = re.compile('<!--.*?-->', re.DOTALL)  # все комментарии
    # а дальше заменяем ненужные куски на пустую строку
    clean_t = regScript.sub("", t)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    return clean_t


def get_article(page):
    ##Извлекает текст самой статьи
    d_text = re.search(r'<div>\n<p>(.*</p>\n.*)(\n)*(\t)*<p></p>', page, flags=re.DOTALL).group(1)
    c_text = html.unescape(clean(d_text))
    return c_text


def make_inf(inf_dict):
    ##Собирает информацию в одну строку, чтобы было удобно записывать в файл
    inf = '@au Noname\n@ti '+inf_dict['title']+'\n@da '+inf_dict['created']+'\n@topic '+inf_dict['topic']+'\n@url '+inf_dict['url']+'\n'
    return inf


def get_inf(page, url):
    ##Вытаскивает информацию со страницы. Автора специальным тегом не размечают и указывают не везде, поэтому его не ищем.
    inf_dict = {}
    inf_dict['title'] = re.search(r'<h2>(.*)?</h2', page).group(1)
    inf_dict['created'] = re.search(r'<div class="mndata">(.*)?</div>', page).group(1)
    inf_dict['topic'] = re.search(r'<h1>(.*)?</h1>', page).group(1).lower()
    inf_dict['url'] = url
    return inf_dict


## Функции работы с файлами

def make_d(created, i):
    ##Делает папку, возвращает путь к файлу
    date = created.split('.')
    directory = os.path.join('plain', date[-1], date[-2])
    if not os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, str(i)+'.txt')


def write_f(text, inf, f_path):
    with open(f_path, 'a', encoding='utf-8') as f:
        f.write(inf+'\n')
        f.write(text)


def write_str(inf_dict, path):
    with open('metadata.csv', 'a', encoding = 'utf-8') as f:
        f.write('\t'.join([path, '', '', '', inf_dict['title'], inf_dict['created'], 'публицистика', '', '', inf_dict['topic'], '', 'нейтральный', 'н-возраст', 'н-уровень', 'районная', inf_dict['url'], 'Сурские просторы', '', inf_dict['created'][-4::], 'газета', 'Россия', 'Пензенская область', 'ru\n']))
    print('записал строку')


## Функции работы с интернетом

def make_links(arr_of_match):
    arr = []
    for i in arr_of_match:
        a = 'http://www.surskieprostori.ru'+i.group(1)
        arr.append(a)
    return arr


def getlinks():
    ##Ходит по ссылкам из массива и пытается с ними работать
    form = 'http://bash.im/index/n'
    arr_texts = []
    for i in range(1299, 1200):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        req = urllib.request.Request(form%(i), headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            arr = re.finditer(r'<div class="text">(.*)?</div>', html)
        n_arr = [m.group(1) for m in arr]
        texts = r'\n'.join(n_arr)
        with open(str(i)+'.txt', 'w', encoding='utf-8') as f:
            f.write(texts)
    return texts


def get(link):
    ## выгружает страницу в память
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(link, headers={'User-Agent': user_agent})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('cp1251')
    return html


def getpages(arr_links):
    ##Делает со страницами все, считает количество слов и количество прорпущенных статей.
    counter = 0
    except_counter = 0
    arr_inf = []
    for i in range(len(arr_links)):
        ht = get(arr_links[i])
        inf = get_inf(ht, arr_links[i])
        try:
            text = get_article(ht)
        except:
            print('Не работает! ', arr_links[i])
            except_counter += 1
            pass
        counter += len(text.split(' '))
        path = make_d(inf['created'], i)
        information = make_inf(inf)
        write_f(text, information, path)
        write_str(inf, path)
        print(counter)
    print('Столько пропущено', except_counter)
    return arr_inf


def make_csv():
    with open('metadata.csv', 'w', encoding = 'utf-8') as f:
        f.write('\t'.join(['path', 'author', 'sex', 'birthday', 'header', 'created', 'sphere', 'genre_fi','type', 'topic', 'chronotop', 'style', 'audience_age', 'audience_level', 'audience_size', 'source', 'publication', 'publisher', 'publ_year', 'medium', 'country', 'region', 'language\n']))
## стемминг
def mystem_plain():
    mystem = r'mystem.exe'
    for root, dirs, files in os.walk('plain'):
        for f in files:
            goalDir = root.replace('plain', 'mystem-plain')
            if not os.path.exists(goalDir):
                os.makedirs(goalDir)
            mystem_plain = mystem + ' ' + root + os.sep + f + ' ' + goalDir + os.sep + f + ' -cid --format text'
            os.system(mystem_plain)


def mystem_xml():
    mystem = r'mystem.exe'
    for root, dirs, files in os.walk('plain'):
        for f in files:
            goalDir = root.replace('plain', 'mystem-xml')
            if not os.path.exists(goalDir):
                os.makedirs(goalDir)
            mystem_plain = mystem + ' ' + root + os.sep + f + ' ' + goalDir + os.sep + f.replace('.txt', '.xml') + ' -cid --format xml'
            os.system(mystem_plain)


getlinks()
