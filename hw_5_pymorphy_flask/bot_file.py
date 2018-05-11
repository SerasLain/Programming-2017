import pymorphy2
import random
import json
from flask import Flask
from flask import render_template, request

app = Flask(__name__)
morph = pymorphy2.MorphAnalyzer()

def write_dictionary(data):
    with open('data.json', 'w', encoding='utf-8') as fh: #открываем файл на запись
        fh.write(json.dumps(data, ensure_ascii=False)) #преобразовываем словарь data в unicode-строку и записываем в файл
    print('Записано!')

def clean_freq():
    with open('1grams-3.txt', 'r', encoding='utf-8') as f:
        a = f.read().strip('\n')
    word_arr = [i.lower().split('\t') for i in a.split('\n')]
    print(word_arr)
    words = set([i[1] for i in word_arr if int(i[0]) > 200])
    return words


def get_words():
    #Делает словарь, где ключи - постоянные признаки слов, а значения - возможные леммы.
    lemmas_dict = {}
    with open('./1grams-3.txt', 'r', encoding='utf-8') as f:
        words = clean_freq()
    for word in words:
        const = str(morph.parse(word)[0].tag).split(' ')[0]
        lemma = str(morph.parse(word)[0].normal_form)
        print(const+' '+lemma)
        if const in set(lemmas_dict.keys()):
            lemmas_dict[const].append(lemma)
        else:
            options = []
            options.append(lemma)
            lemmas_dict[const] = options
    write_dictionary(lemmas_dict)


def get_new(const, lemmas_dict):
    word = morph.parse(random.choice(lemmas_dict[const]))[0].normal_form
    return word


def change_word(word, lemmas_dict):
    grammar = str(morph.parse(word)[0].tag).split(' ')
    print(grammar)
    #Нулевой элемент - это постоянные признаки слова, а первый - изменяемые.
    new_word = None
    while new_word == None:
        new_lemma = get_new(grammar[0], lemmas_dict)
        if len(grammar) != 1:
            flexible = set(grammar[1].split(','))
            print(flexible)
            new_word = (morph.parse(new_lemma)[0].inflect(flexible))
            new_word = new_word.word
        else:
            new_word = new_lemma
    return new_word

def make_sentence(sentence, lemmas_dict):
    sentence = sentence.lower()
    sent_arr = [word.strip('.,:"!?-();') for word in sentence.split(' ') if word not in set('.,—-–:;')]
    new_sent_arr = []
    for i in sent_arr:
        new_word = change_word(i, lemmas_dict)
        new_sent_arr.append(new_word)
    for i in range(len(sent_arr)):
        sentence = sentence.replace(sent_arr[i], new_sent_arr[i])
        sentence = sentence.capitalize()
    return sentence

def get_from():
    with open('data.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
        data = json.load(fh) #загружаем из файла данные в словарь data
    return data


def black_box(sentence):
    #Функция, которая работает с предложением.
    #get_words()
    lemmas_dict = get_from()
    try:
        new_sent = make_sentence(sentence, lemmas_dict)
    except:
        new_sent = "Что-то пошло не так. Проверьте орфографию, попробуйте еще раз или введите другое предложение."
    return(new_sent)

##Обертка - сайт на фласке (не вышло чет бота)

@app.route('/')
def index():
    new_sentence = ""
    if request.args:
        sentence = request.args.get('sentence')
        if sentence != "":
            new_sentence = black_box(sentence)
    return render_template('index.html', sentence=new_sentence)


if __name__ == '__main__':
    app.run(debug=True)
