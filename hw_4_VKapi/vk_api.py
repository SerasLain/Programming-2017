import datetime
import urllib.request
import json
import sqlite3
import matplotlib.pyplot as plt

##Вроде бы всё умеет, и собирает всю информацию в БД. Графики получаются не очень хорошие (но, возможно, я не поняла, что именно надо было визуализировать)
access_token = 'd95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c'
conn = sqlite3.connect('perawki_plus.db')
c = conn.cursor()

## Делают базу данных и наполняют первую её таблицу инфой про посты
def create_database():
    c.execute("CREATE TABLE Posts (Post_id, Author_id, text TEXT)")
    c.execute("CREATE TABLE Comments (Post_id, Author_id, comment_text TEXT)")
    c.execute("CREATE TABLE Authors (Author_id, age, city)")
    conn.commit()


def show_db():
    ## Техническая функция, чтобы проверить, все ли нормально в таблице
    c.execute('SELECT * FROM Comments')
    a = c.fetchall()
    return a


def get_posts(n):
    request = 'https://api.vk.com/method/wall.get?v=5.74&domain=perawki&access_token=d95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c&offset='+str(n)+'&post'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(request, headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(req)
    json_arr = response.read().decode('utf-8')
    a = json.loads(json_arr)
    print(n)
    return a['response']


def information_post(response):
    n = response['count']
    posts = response['items']
    for d in posts:
        post_id = d['id']
        auth_id = d['from_id']
        text = d['text']
        print(text)
        write_Posts(post_id, auth_id, text)
    return n


def make_Posts():
    count = information_post(get_posts(0))
    if count > 100:
        offsets = range(100, count+1, 100)
        for n in offsets:
            information_post(get_posts(n))


def write_Posts(post_id, auth_id, text):
    c.execute("INSERT INTO Posts VALUES (?,?,?)", (post_id, auth_id, text))
    conn.commit()

## Берут id постов и заполняют таблицу комментариями
def get_post_ids():
    c.execute("SELECT Post_id FROM Posts")
    ids = c.fetchall()
    conn.commit()
    return ids

def get_comments(n, id):
    request = 'https://api.vk.com/method/wall.getComments?v=5.74&owner_id=-28122932&access_token=d95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c&offset='+str(n)+'&post_id='+str(id)
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(request, headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(req)
    json_arr = response.read().decode('utf-8')
    a = json.loads(json_arr)
    print(n)
    return a['response']


def write_comments(post_id, author_id, comment_text):
    c.execute("INSERT INTO Comments VALUES (?,?,?)", (post_id, author_id, comment_text))
    conn.commit()


def information_comments(response, post_id):
    n = response['count']
    comments = response['items']
    for d in comments:
        if d['text'] != '':
            write_comments(str(post_id), d['from_id'], d['text'])
            print(d['text'])
    return n


def make_Comments(post_ids):
    for i in post_ids:
        count = information_comments(get_comments(0, i[0]), i[0])
        if count > 100:
            print('GET!!!!!!! ', i)
            offsets = range(100, count+1, 100)
            for n in offsets:
                information_comments(get_comments(n, i[0]), i[0])

## Делают таблицу с информацией обо всех авторах, которые встречались в комментариях или записях. (Отдельная таблица c уникальными id - чтобы меньше запросов к вк делать)
def get_authors():
    c.execute("SELECT Author_id FROM Posts")
    post_authors = c.fetchall()
    c.execute("SELECT Author_id FROM Comments")
    comment_authors = c.fetchall()
    all_authors = set()
    for i in post_authors:
        all_authors.add(i[0])
    for i in comment_authors:
        all_authors.add(i[0])
    conn.commit()
    return all_authors


def information_author(id):
    if id > 0:
        request = 'https://api.vk.com/method/users.get?v=5.74&access_token=d95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c&fields=city,bdate&user_ids='+str(id)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        req = urllib.request.Request(request, headers={'User-Agent': user_agent})
        response = urllib.request.urlopen(req)
        json_arr = response.read().decode('utf-8')
        print(id)
        print(json_arr)
        a = json.loads(json_arr)['response'][0]
        if 'bdate' in a:
            bdate = a['bdate'].split('.')
            if len(bdate) != 3:
                age = 'Unknown'
            else:
                ## Костыль: не учитывается, что длина года бывает разной. Но нам и не критично некоторое различие
                now = datetime.datetime.today()
                then = datetime.datetime(int(bdate[2]),int(bdate[1]),int(bdate[0]))
                delta = now - then
                age = str(delta.days // 365)
        else:
            age = 'Unknown'
        if 'city' in a:
            city = a['city']['title']
        else:
            city = 'Unknown'
    else:
        age = 'Unknown'
        request = 'https://api.vk.com/method/groups.getById?v=5.74&access_token=d95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c&fields=city&group_ids='+str(-id)
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        req = urllib.request.Request(request, headers={'User-Agent': user_agent})
        response = urllib.request.urlopen(req)
        json_arr = response.read().decode('utf-8')
        print(id)
        print(json_arr)
        a = json.loads(json_arr)['response'][0]
        if 'city' in a:
            city = a['city']['title']
        else:
            city = 'Unknown'
    return (age, city)


def write_authors(authors):
    for i in authors:
        inf = information_author(i)
        print(inf)
        c.execute("INSERT INTO Authors VALUES (?,?,?)", (i, inf[0], inf[1]))
        conn.commit()


##Работать с таблицами и строить графики
def get_all_comments(id):
    #Берет id поста и вынимает из БД все комментарии к этому посту, возвращает массив строк
    c.execute("SELECT comment_text FROM Comments WHERE post_id='" + str(id)+"'")
    a = c.fetchall()
    conn.commit()
    texts = [i[0] for i in a]
    return texts


def count_m(comments):
    #Считает среднюю длину поста
    if comments == []:
        return 0
    else:
        len_arr = []
        for i in comments:
            i.replace('\n', ' ')
            a = i.split(' ')
            n = len(a)
            len_arr.append(n)
        m = sum(len_arr) / len(len_arr)
        return m


def get_text(id):
    #Извлекает текст поста из БД по айди поста
    c.execute('SELECT text FROM Posts WHERE Post_id='+ str(id))
    text = c.fetchall()
    return text[0]


def make_axes_length(arr_post_ids):
    #Делает график про длину поста и среднюю длину комментария
    text_l = []
    comment_m = []
    for i in arr_post_ids:
        id = i[0]
        l = count_m(get_text(id))
        m = count_m(get_all_comments(id))
        print(l, m, sep=' ')
        text_l.append(l)
        comment_m.append(m)
    print(text_l)
    for x, y in zip(text_l, comment_m):
        plt.scatter(x, y)
    plt.xlabel('Длина поста')
    plt.ylabel('Длина комментария')
    plt.savefig('length.png', format = 'png')


def get_person_ids():
    c.execute('SELECT Author_id FROM Authors')
    ids = [i[0] for i in c.fetchall()]
    return ids


def get_person_posts(author_id):
    c.execute("SELECT text FROM Posts WHERE Author_id ="+ str(author_id))
    text = [i[0] for i in c.fetchall()]
    return count_m(text)


def get_person_comments(author_id):
    c.execute('SELECT comment_text FROM Comments WHERE Author_id='+ str(author_id))
    text = [i[0] for i in c.fetchall()]
    return count_m(text)
    ##Доделать. Логика такая: получить и посчитать сразу всё среднее аналогично предыдущему, потом получить все комменты по айди и сделать для них то же самое, а потом построить всю эту муть

def make_person(person_ids):
    ##Делает график для каждого id соотношение средней длины коммента и поста. Выходит скучным: на стене пирожков+ постит только само сообщество.
    text_l = []
    comment_m = []
    for id in person_ids:
        l = get_person_posts(id)
        m = get_person_comments(id)
        print(l, m, sep=' ')
        text_l.append(l)
        comment_m.append(m)
    print(text_l)
    for x, y in zip(text_l, comment_m):
        plt.scatter(x, y)
    plt.xlabel('Длина поста')
    plt.ylabel('Длина комментария')
    plt.savefig('person.png', format = 'png')


def get_ages():
    c.execute('SELECT age FROM Authors')
    age_arr = set([i[0] for i in c.fetchall()])
    print(age_arr)
    age_dict = {}
    for age in age_arr:
        c.execute("SELECT Author_id FROM Authors WHERE age="+"'"+age+"'")
        persons = [i[0] for i in c.fetchall()]
        comm = []
        posts = []
        for id in persons:
            comm.append(get_person_comments(id))
            posts.append(get_person_posts(id))
        if comm != []:
            comm_m = sum(comm) / len(comm)
        else:
            comm_m = 0
        if posts != []:
            post_m = sum(posts) / len(posts)
        else:
            post_m = 0
        age_dict[age] = (comm_m, post_m)
    print(age_dict)
    return age_dict


def make_age(age_dict):
    names_arr = age_dict.keys()
    print(names_arr)
    comment_m = [age_dict[name][0] for name in names_arr]
    post_m = [age_dict[name][1] for name in names_arr]
    for x, y, d in zip(post_m, comment_m, names_arr):
        plt.scatter(x, y)
        plt.text(x, y, d) # +0.1 - это чтобы текст не наползал на маркер, а отрисовывался чуть правее
    plt.xlabel('Длина поста')
    plt.ylabel('Длина комментария')
    plt.savefig('age.png', format = 'png')

def get_cities():
    #Если на клетке с тигром написано "Заяц" - не верь глазам своим
    c.execute('SELECT city FROM Authors')
    city_arr = set(i[0] for i in c.fetchall())
    print(city_arr)
    city_dict = {}
    for city in city_arr:
        c.execute("SELECT Author_id FROM Authors WHERE city="+"'"+city+"'")
        persons = [i[0] for i in c.fetchall()]
        comm = []
        posts = []
        for id in persons:
            comm.append(get_person_comments(id))
            posts.append(get_person_posts(id))
        if comm != []:
            comm_m = sum(comm) / len(comm)
        else:
            comm_m = 0
        if posts != []:
            post_m = sum(posts) / len(posts)
        else:
            post_m = 0
        print(city)
        city_dict[city] = (comm_m, post_m)
    print(city_dict)
    return city_dict

def make_city(city_dict):
    print(city_dict)
    names_arr = city_dict.keys()
    print(names_arr)
    comment_m = [city_dict[name][0] for name in names_arr]
    post_m = [city_dict[name][1] for name in names_arr]
    for x, y, d in zip(comment_m, post_m, names_arr):
        plt.scatter(x, y)
        plt.text(x, y, d)
    plt.xlabel('Длина комментария')
    plt.ylabel('Длина поста')
    plt.savefig('city.png', format = 'png')


def main():
    #Создание и наполнение БД
    create_database()
    make_Posts()
    make_Comments(get_post_ids())
    write_authors(get_authors())
    #Графики
    make_axes_length(get_post_ids())
    make_person(get_person_ids())
    make_age(get_ages())
    make_city(get_cities())
    conn.close()

if __name__ == '__main__':
    main()
