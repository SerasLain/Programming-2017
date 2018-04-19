## Видят боги, я не хотела это писать
from flask import Flask
from flask import render_template, request
import html
import urllib.request
import re
import sqlite3
from pymystem3 import Mystem
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
mystem = Mystem()
##Создаем БД для словаря
def create_database():
    conn = sqlite3.connect('doref_dictionary.db')
    c = conn.cursor()
    c.execute("CREATE TABLE Words (modern, old)")
    conn.commit()
    conn.close()


def insert_word(tup):
    conn = sqlite3.connect('doref_dictionary.db')
    c = conn.cursor()
    c.execute("INSERT INTO Words VALUES (?,?)", tup)
    conn.commit()
    conn.close()


def get(link):
    ## выгружает страницу в память
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(link, headers={'User-Agent': user_agent})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    return html


def make_links():
    ##Это моя лень почистить строку руками. Делает массив ссылок на страницы с буквами
    text = r'<a href="a.html">А</a> * <a href="b.html">Б</a> * <a href="v.html">В</a> * <a href="g.html">Г</a> * <a href="d.html">Д</a> * <a href="e.html">Е</a> * <a href="sch.html">Ж</a> * <a href="z.html">З</a> * <a href="i.html">И</a> * <a href="k.html">К</a> * <a href="l.html">Л</a> * <a href="m.html">М</a> * <a href="n.html">Н</a> * <a href="o.html">О</a> * <a href="p.html">П-Пл</a> * <a href="po.html">По</a> * <a href="pr.html">Пр-Пя</a><br><a href="r.html">Р</a> * <a href="s.html">С-Сл</a> * <a href="sm.html">См-Сю</a> * <a href="t.html">Т</a> * <a href="u.html">У</a> * <a href="f.html">Ф</a> * <a href="x.html">Х</a> * <a href="c.html">Ц</a> * <a href="ch.html">Ч</a> * <a href="sh.html">Ш-Щ</a> * <a href="ya.html">Э-Я</a></h4>'
    a = re.finditer('<a href="(.*?)">', text)
    arr = ['http://slovnik.narod.ru/old/slovar/'+i.group(1) for i in a]
    print('Links!')
    return arr

def get_text(page):
    ##проходит по страницам, заполняет БД
    regex = r'<table border=1 width=100%>(.*?)</table>'
    table = re.search(regex, page, flags=re.DOTALL).group(0)
    regex = r'<td>(.*?)</td>\n\s+<td>(.*?)</td>'
    arr = re.finditer(regex, table)
    arr_pairs = [(i.group(1), i.group(2).strip()) for i in arr]
    print(arr_pairs)
    for i in arr_pairs:
        print(i)
        insert_word(i)



def get_pages(arr_links):
    for i in range(len(arr_links)):
        print(arr_links[i])
        page = get(arr_links[i])
        get_text(page)


##Транслитератор
def stem(text):
    arr_dict = mystem.analyze(text)
    return arr_dict

def database_search(lemma, filename="doref_dictionary.db"):
        conn = sqlite3.connect(filename)
        c = conn.cursor()
        old_lemma = c.execute("SELECT old FROM Words WHERE modern=?", (lemma, )).fetchone()
        conn.close()
        return old_lemma

def convert(word, old_lemma, ana):
    if word.startswith('черес') == True:
        word.sub('черес', 'через')
    elif word.startswith('бес'):
        word.sub('бес', 'без')
    elif word.startswith('чрес'):
        word.sub('чрес', 'чрез')
    if word[-1] not in set('йуеыаоэяию'):
        word += 'ъ'
    word_arr = list(word)
    for i in range(len(word_arr)):
        if word_arr[i] != old_lemma[i]:
            if word_arr[i] == 'и':
                word_arr[i]  = old_lemma[i]
            if word_arr[i] == 'ф':
                word_arr[i]  = old_lemma[i]
            if word_arr[i] == 'е' and old_lemma[i] == 'ѣ':
                word_arr[i] = old_lemma[i]
    grammar =  ana[0]['analysis'][0]['gr']
    if grammar[0] in ('A', 'S', 'P'):
        if grammar.find('пр,') != -1 or grammar.find('дат') != -1:
            while True:
                print(word)
                a = word.rfind('е')
                if a == -1:
                    break
                else:
                    word_arr[a] = 'ѣ'
                    break
    n_word = ''.join(word_arr)
    return n_word



def stem_word(word):
    w = mystem.analyze(word)
    print(w)
    lemma = w[0]['analysis'][0]['lex']
    old_lemma = database_search(lemma)
    if old_lemma == None:
        return convert(word, word, w)
    else:
        old_lemma = html.unescape(old_lemma[0].split(' ')[0].strip('.,:('))
        return convert(word, old_lemma, w)


##Сайт
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def result():
    n_word = stem_word(request.args.get('word'))
    return render_template('result.html', n_word=n_word)

def show_db():
    conn = sqlite3.connect('doref_dictionary.db')
    c = conn.cursor()
    print(c.execute("SELECT * FROM Words").fetchmany(10))


def main():
    #create_database()
    #links = make_links()
    links = ['http://slovnik.narod.ru/old/slovar/a.html', 'http://slovnik.narod.ru/old/slovar/b.html', 'http://slovnik.narod.ru/old/slovar/v.html', 'http://slovnik.narod.ru/old/slovar/g.html', 'http://slovnik.narod.ru/old/slovar/d.html', 'http://slovnik.narod.ru/old/slovar/e.html', 'http://slovnik.narod.ru/old/slovar/sch.html', 'http://slovnik.narod.ru/old/slovar/z.html', 'http://slovnik.narod.ru/old/slovar/i.html', 'http://slovnik.narod.ru/old/slovar/k.html', 'http://slovnik.narod.ru/old/slovar/l.html', 'http://slovnik.narod.ru/old/slovar/m.html', 'http://slovnik.narod.ru/old/slovar/n.html', 'http://slovnik.narod.ru/old/slovar/o.html', 'http://slovnik.narod.ru/old/slovar/p.html', 'http://slovnik.narod.ru/old/slovar/po.html', 'http://slovnik.narod.ru/old/slovar/pr.html', 'http://slovnik.narod.ru/old/slovar/r.html', 'http://slovnik.narod.ru/old/slovar/s.html', 'http://slovnik.narod.ru/old/slovar/sm.html', 'http://slovnik.narod.ru/old/slovar/t.html', 'http://slovnik.narod.ru/old/slovar/u.html', 'http://slovnik.narod.ru/old/slovar/f.html', 'http://slovnik.narod.ru/old/slovar/x.html', 'http://slovnik.narod.ru/old/slovar/c.html', 'http://slovnik.narod.ru/old/slovar/ch.html', 'http://slovnik.narod.ru/old/slovar/sh.html', 'http://slovnik.narod.ru/old/slovar/ya.html']
    #наполняем базу данных
    #get_pages(links)
    app.run(debug=True)

if __name__ == '__main__':
    main()


