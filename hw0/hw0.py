import urllib.request
import re

def make_html():
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request('http://www.surskieprostori.ru', headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('cp1251')
    return html


def find_titles(html):
    regex = re.compile('<div class="mnname">.*?</div>', flags=re.U | re.DOTALL)
    title_arr = regex.findall(html)
    return title_arr

def clean(array_of_strings):
    clean_arr = []
    regTag = re.compile('<.*?>', flags=re.U | re.DOTALL)
    regSpace = re.compile('\s{2,}', flags=re.U | re.DOTALL)
    for i in array_of_strings:
        clean_i = regSpace.sub('', i)
        clean_i = regTag.sub('', clean_i)
        clean_arr.append(clean_i)
    return clean_arr

def main():
    html = make_html()
    arr = find_titles(html)
    arr = clean(arr)
    for i in arr:
        print(i)


main()

