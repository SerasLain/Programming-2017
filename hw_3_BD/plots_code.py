## Тут типа код
## Тут типа надо еще графиков дографичить
import sqlite3
import matplotlib.pyplot as plt

def create_database():
    conn = sqlite3.connect('new_hittite.db')
    c = conn.cursor()
    c.execute("CREATE TABLE Words (id, Lemma, Wordform, Glosses)")
    c.execute("CREATE TABLE Glosses (id, Gloss TEXT, Meaning TEXT)")
    c.execute("CREATE TABLE word_gloss (word_id, gloss_id)")
    conn.commit()
    conn.close()


def get_glosses():
    with open('Glossing_rules.txt', 'r', encoding = 'utf-8') as f:
        glosses = f.readlines()
    gloss_arr = [i.split(' — ') for i in glosses]
    return gloss_arr


def make_gloss_dict(gloss_arr):
    gloss_dict = {}
    for i in gloss_arr:
        gloss_dict[i[0]] = i[1]
    return gloss_dict


def write_glosses(gloss_arr):
    conn = sqlite3.connect('new_hittite.db')
    c = conn.cursor()
    for i in range(len(gloss_arr)):
        c.execute("INSERT INTO Glosses VALUES (?,?,?)", (i, gloss_arr[i][0], gloss_arr[i][1].strip()))
    conn.commit()
    conn.close()


def write_wordforms():
    conn = sqlite3.connect('hittite.db')
    c = conn.cursor()
    ## connection with new database
    n_conn = sqlite3.connect('new_hittite.db')
    n_c = n_conn.cursor()
    c.execute("SELECT * FROM wordforms")
    rows = c.fetchall()
    for i in range(len(rows)):
        n_c.execute("INSERT INTO Words VALUES (?,?,?,?)", (i, rows[i][0], rows[i][1], rows[i][2]))
    n_conn.commit()
    n_conn.close()
    print('Done')

def write_wordgloss():
    conn = sqlite3.connect('new_hittite.db')
    c = conn.cursor()
    c.execute("SELECT id, Glosses FROM Words")
    rows = c.fetchall()
    row_arr = []
    for i in rows:
        row_arr.append([i[0], [l for l in i[1].split('.') if l.isupper() == True]])
    for i in row_arr:
        if i[1] != []:
            for gloss in i[1]:
                print(gloss)
                id_gloss = c.execute("SELECT id FROM Glosses WHERE Gloss=?", (gloss,)).fetchone()
                print(i[0], id_gloss)
                if id_gloss != None:
                    c.execute("INSERT INTO word_gloss VALUES (?,?)", (i[0], id_gloss[0]))
                else:
                    ##Это такой костыль: про то, что чего-то надо руками размечать, в задании не было - ну я и не размечаю. Только дописываю в БД неизвестные глоссы, чтобы у них был id и было чего визуализировать
                    n = len(c.execute("SELECT id FROM Glosses").fetchall())
                    c.execute("INSERT INTO Glosses VALUES (?,?,?)", (n, gloss, 'NonPOS'))
                    c.execute("INSERT INTO word_gloss VALUES (?,?)", (i[0], n))
    print('Done')
    conn.commit()
    conn.close()


## Веселые картинки: считаем глоссы.
def count_glosses():
    conn = sqlite3.connect('new_hittite.db')
    c = conn.cursor()
    arr = [i[0] for i in c.execute("SELECT gloss_id FROM word_gloss").fetchall()]
    dictionary = {i: arr.count(i) for i in set(arr)}
    gloss_notation = {i[0]:i[1] for i in c.execute("SELECT * FROM Glosses").fetchall()}
    conn.close()
    gloss_count = {}
    for i in dictionary:
        gloss_count[gloss_notation[i]] = dictionary[i]
    return gloss_count

def let_my_people_go(gloss_count):
    ##И разошлись перед Моисеем глоссы по велению Божьему...
    ##делит словарь со всеми глоссами на два словаря: словарь с частями речи и словарь с другими граммемами
    conn = sqlite3.connect('new_hittite.db')
    c = conn.cursor()
    arr_nonpos = [i[0] for i in c.execute("SELECT Gloss FROM Glosses WHERE Meaning=?", ('NonPOS', )).fetchall()]
    POS_dict = {}
    NonPOS_dict = {}
    for i in gloss_count:
        if i not in arr_nonpos:
            POS_dict[i] = gloss_count[i]
        else:
            NonPOS_dict[i] = gloss_count[i]
    return POS_dict, NonPOS_dict

def plot_dictionary(dictionary):
    names = sorted(dictionary.keys())
    X = list(range(0, len(dictionary)))
    Y = [dictionary[name] for name in names]
    for x, y, d in zip(X, Y, names):
        plt.scatter(x, y)
        plt.text(x+0.1, y+0.1, d) # +0.1 - это чтобы текст не наползал на маркер, а отрисовывался чуть выше и правее
    plt.show()

def plot(gloss_count):
    POS_names, NonPOS_names = let_my_people_go(gloss_count)
    plt.subplot(211)
    plot_dictionary(POS_names)
    plt.subplot(212)
    plot_dictionary(NonPOS_names)




def main():
    create_database()
    write_glosses(get_glosses())
    write_wordforms()
    write_wordgloss()
    plot(count_glosses())

if __name__ == "__main__":
    main()
