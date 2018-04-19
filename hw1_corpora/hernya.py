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

@app.route('/')
def index():
    return ''
