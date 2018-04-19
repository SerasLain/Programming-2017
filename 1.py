##Переписывает таблицу
def make_csv():
    ##делает таблицу с нужной шапкой
    with open('results.csv', 'w', encoding='utf-8') as f:
        f.write('rsp,mtd,word,res\n')
    print('Таблица сформирована!')

def read_csv():
    with open(r'C:\Users\1\Downloads\data_clean.csv', 'r', encoding = 'utf-8') as f:
        arr_lines = f.readlines()
    arr_table = [i.strip().split(',') for i in arr_lines]
    return arr_table

def get_indexes(arr_table):
    ##Вытаскивает индексы, по которым нужно будет обращаться к элементам массива - строки в таблице
    arr_indexes = []
    for i in range(len(arr_table[0])):
        print(arr_table[0][i])
        if arr_table[0][i] in ['age','gender','RegionBorn','RegionLife','education']:
            arr_indexes.append(i)
    return arr_indexes

def write_string(arr):
    line = ','.join(arr)
    with open('results.csv', 'a', encoding='utf-8') as f:
        f.write(line)


def write_csv(arr_table):
    indexes = get_indexes(arr_table)
    print(indexes)
    for i in range(1, len(arr_table)):
        print(arr_table[i])
        ##Лень: костыль, который заменяет названия регионов из удобных в нормальные
        for j in indexes:
            if arr_table[i][j] == 'ЛО':
                arr_table[i][j] = 'Санкт-Петербург и Ленинградская область'
            elif arr_table[i][j] == 'МО':
                arr_table[i][j] = 'Москва и Московская область'
            elif arr_table[i][j] == 'В':
                arr_table[i][j] = 'Восточнее Урала'
            elif arr_table[i][j] == 'З':
                arr_table[i][j] = 'Западнее Урала'
            line = []
            line.append(str(i))
            line.append(arr_table[0][j])
            line.append(arr_table[i][j]+'\n')
            write_string(','.join(line))
            print(i, j,'Done!')


def write_csv_results(arr_table):
    indexes = sorted(index_dict.keys())
    for i in range(1, len(arr_table)):
        print(i)
        for key in indexes:
            print(key)
            ##Здесь у нас была сложная материя: нужно было по одной колонке построить разные графики, то есть развести данные в разныые переменные в зависимости от значения другой колонки.
            if key == "zhad_bar_dl":
                if arr_table[i][1] == 'Б':
                    line = [str(i), 'Опрос в гугл-форме', key, arr_table[i][index_dict[key]]+'\n']
                    print(line)
                    write_string(line)
            elif key == "zhad_ogur_dl":
                if arr_table[i][1] == 'О':
                    line = [str(i), 'Опрос в гугл-форме', key, arr_table[i][index_dict[key]]+'\n']
                    write_string(line)
            else:
                line = [str(i), 'Опрос в гугл-форме', key, arr_table[i][index_dict[key]]+'\n']
                write_string(line)


##Мне показалось, что проще руками их вытащить из списка пронумерованных, что я и сделала
index_dict = {"zhad_bar":1,"zhad_bar_dl":2,"zhad_ogur_dl":2,"plaksa_vaksa":4,"plaksa_dl":5,"obmanuli_kogo":10,"obmanuli_na":11,"obmanuli_dlina":12,"ryova_dl":15,"ryova":14}

def main():

    make_csv()
    write_csv_results(read_csv())

if __name__ == '__main__':
    main()
