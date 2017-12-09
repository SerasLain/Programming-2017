import pandas as pd
##Хотела прикрутить более кошерную статистику, но как-то не сложилось

from flask import Flask
from flask import render_template, request
import os


app = Flask(__name__)

def make_csv():
    ##Делает заголовки и csv
    with open('results.csv', 'w', encoding = 'utf-8') as f:
            f.write('Возраст;Место рождения;Место жительства;Пол;Зарядник;Пауэрбэнк;Шнур;Термокружка;Парка;Трансформер\n')


@app.route('/')
def index():
    if request.args:
        if 'results.csv' not in os.listdir('.'):
            make_csv()
        else:
            f = open('results.csv', 'a', encoding='utf-8')
            ##Разделитель - ;
            f.write('%d;%s;%s;%s;%s;%s;%s;%s;%s;%s\n' % (int(request.args.get('age')), request.args.get('region_born'), request.args.get('region_now'), request.args.get('gender'), request.args.get('zaryadnik'), request.args.get('power'), request.args.get('shnur'), request.args.get('termo'), request.args.get('parka'), request.args.get('trans')))
            f.close()
    return render_template('index.html')

@app.route('/stats')
def stats():
    # Статистика по заполненным анкетам
    data = pd.read_csv('results.csv', sep=';')
    total_count = len(data['Возраст'])
    av_age =  sum(data["Возраст"])/total_count
    regions = data["Место жительства"]
    region_count = len(set(regions))
    all_regions = ', '.join(set(regions))
    def most_regions():
        # И редкие тоже считает!
        d = {}
        for i in regions:
            if i not in d:
                d[i] = 1
            else:
                d[i] += 1
        arr_rares = [str(k) for k in d if d[k] == 1]
        most = max(d.values())
        arr_regions = [str(k) for k in d if d[k] == most]
        return (', '.join(arr_regions), ', '.join(arr_rares))
    q_region = most_regions()[0]
    r_region = most_regions()[1]
    ## Статистика по результатам
    ##А нету ее(
    return render_template('stats.html', total_count = total_count, av_age = av_age, region_count = region_count, q_region=q_region, regions = all_regions, r_regions = r_region)

@app.route('/json')
##json со всеми введенными данными, организован, чтобы красиво на странице выглядеть. Чтобы ничего не поплыло, при машинной обработке достаточно будет тэги поубирать.
def json():
    with open('results.csv','r', encoding='utf-8') as f:
        jsonAr = []
        data = f.readlines()
        for l in range(1, len(data)):
            info = [i.replace(' ', '_') for i in data[l].strip().split(';')]
            jsonLine = '<tab1>"age": ' + str(info[0]) + ',<br /></tab1>' + '<tab1>"region_born": \"' + info[1] + '\",<br /></tab1>' + '<tab1>"region": \"' + info[2] + '\",<br /></tab1>' + '<tab1>"gender": \"' + info[3] + '\",<br /></tab1>' + '<tab1>"zaryadnik": \"' + info[4] + '\",<br /></tab1>' + '<tab1>"powerbank" \"' + info[5] + '\",<br /></tab1>' + '<tab1>"shnur": \"' + info[6] + '\",<br /></tab1>' + '<tab1>"termokruzhka": \"' + info[7] + '\",<br /></tab1>' + '<tab1>"parka": \"' + info[8] + '\",<br /></tab1>' + '<tab1>"notebook_transformer": \"' + info[9] + '\"<br /></tab1>'
            jsonAr.append(jsonLine)
    return render_template('json.html', jsonar=jsonAr)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results')
def results():
    search_req = {3:request.args.get('searchGender'), 1:request.args.get('searchRegionBorn'), 2:request.args.get('searchRegionLife'), 0:request.args.get('searchAge')}
    search_options = {k:search_req[k] for k in search_req if search_req[k] != ''}
    if 0 in search_options.keys():
        ##Зададим диапазон для возраста
        age_options = {'yng': request.args.get('younger'), 'old':request.args.get('older'), 'equ':request.args.get('equal')}
        age_search = int(search_options[0])
        min = age_search
        max = age_search + 1
        if age_options['yng'] == 'on':
            min = 0
        if age_options['old'] == 'on':
            max = 100
        age_possible = set(range(min, max))
        if age_options['equ'] != 'on':
            age_possible.discard(age_search)
    with open('results.csv', 'r', encoding='utf-8') as f:
        data = f.read().strip().split('\n')
    resultArr = []
    for index in range(1, len(data)):
        iter_row = data[index].split(";")
        validator = True
        for key in search_options:
            if key == 0:
                if int(iter_row[0]) not in age_possible:
                    validator = False
            else:
                if iter_row[key] != search_options[key]:
                    validator = False
        if validator == True:
            resultArr.append(iter_row)
    if resultArr == []:
        resultArr.append(['Ничего не нашлось, уточните параметры запроса','','','','','','','','',''])
    return render_template('results.html', resultAr=resultArr)



if __name__ == '__main__':
    app.run(debug=False)
