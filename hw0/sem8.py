from flask import Flask
from flask import url_for, render_template, request, redirect


app = Flask(__name__)

def open_langs():
    with open(r'C:\Users\1\Downloads\langs_codes.csv', 'r', encoding='utf-8') as f:
        codes = f.readlines()
        dict_codes = {}
        for string in codes:
            a = string.split(',')
            dict_codes[a[0]] = a[1]
    return dict_codes

@app.route('127.0.0.1:5000/')
def index():
    dict = open_langs()
    return render_template('index.html', dict = dict)

@app.route('127.0.0.1:5000/langs/not_found')

@app.route('127.0.0.1:5000/lang/<lang>')
def lang(lang = input(), dict = open_langs()):
    n_d = {}
    for key, value in dict.items():
        if key.startswith(lang):
            n_d[key] = value
    if n_d == {}:
       redirect(url_for('not found'))
    else:
        return render_template('index.html', dict = n_d)


if __name__ == '__main__':
    app.run(debug=True)
