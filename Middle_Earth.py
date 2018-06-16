import re
import random
from collections import defaultdict
from flask import Flask
from flask import render_template, request
#Функции самой модели, немного подправленные мной.
#Токенизация через регулярки. Не знаю, что быстрее - так или через сплиты
#Честно говоря, я понимаю генераторы чуть меньше, чем нихрена...
r_alphabet = re.compile(u'[а-яА-Я0-9-]+|[.,:;?!]+')
app = Flask(__name__)

def make_lines():
    with open(r'T_corp.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()
    for line in data:
        yield line

lines = make_lines()


def gen_tokens(lines):
    for line in lines:
        try:
            for token in r_alphabet.findall(line):
                yield token
        except:
            print(line)

tokens = gen_tokens(lines)


def gen_trigrams(tokens):
    left, middle = '$', '$'
    for last in tokens:
        yield left, middle, last
        if last in '.!?':
             yield middle, last, '$'
             yield last, '$','$'
             left, middle = '$', '$'
        else:
            left, middle = middle, last

def train(trigrams):
    bi = defaultdict(lambda: 0.0)
    tri = defaultdict(lambda: 0.0)

    for (t0, t1, t2) in trigrams:
        bi[(t0, t1)] += 1
        tri[(t0, t1, t2)] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[(t0, t1)].append((t2, freq/bi[(t0, t1)]))
        else:
            model[(t0, t1)] = [(t2, freq/bi[(t0, t1)])]
    return model


def parse_reply(sentence):
    s = [word.lower().strip('.,?!:;()') for word in sentence.split(' ')]
    return s

def sort_by_P(tup):
    return tup[1]

def make_s(t0, t1, model):
    phrase = ''
    while 1:
        vars = sorted(model[(t0, t1)], key = sort_by_P)
        new = random.choice(vars[0:int(len(vars)/2)+1])
        t0, t1 = t1, new[0]
        if t1 == '$':
            break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1
    return phrase.capitalize()

def generate_sentence(model, word):
    while 1:
        question =  parse_reply(word)
        random.shuffle(question)
        for word in question:
            if ('$', word) in model:
                sentence =  make_s('$',word, model)
                break
        sentence = make_s('$', '$', model)
        break
    return sentence


def black_box(request):
    tokens = gen_tokens(make_lines())
    trigrams = gen_trigrams(tokens)
    model = train(trigrams)
    sentence = generate_sentence(model,request)
    return sentence


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
