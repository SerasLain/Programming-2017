import urllib.request
import json

def get_page(request):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(request, headers={'User-Agent': user_agent})
    response = urllib.request.urlopen(req)
    json_arr = response.read().decode('utf-8')
    return json.loads(json_arr)

def get_comments(n):
    req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=31445958&v=5.73&access_token=d95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c&post_id='+str(n))
    response = urllib.request.urlopen(req)
    comments = response.read().decode('utf-8')
    return json.loads(comments)

def mine():
    ##json_arr = json.loads(get_page())
    ##posts = json_arr['response']['items']
    ##print(posts)
    ##arr = []
    ##for i in posts:
    ##  items = get_comments(i['id'])['response']['items']
      ##if items != []:
        ##  arr.append(items)
    ##print(arr)
    texts = []
    ##for i in arr:
      ##  for k in i:
        ##    texts.append(k['text'])
    ##print(texts)
    ##words = []
    ##for i in texts:
      ##  for w in i.split(' '):
        ##    words.append(w.strip('.,?_-:;!'))
    quant = {}
    ##Надо доделать - частотный словарь
    ##Получить все посты
    ##получить
    offsets = [0, 1000, 2000, 3000, 4000]
    users = set()
    for off in offsets:
        req = urllib.request.Request('https://api.vk.com/method/groups.getMembers?group_id=dormitory8hse&v=5.23&access_token=d95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c&offset=' + str(off))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        users = users | set(data['response']['items'])
    print(len(users))
    cities = []
    i = 0
    for user in users:
        if i > 100:
            break
        req = urllib.request.Request('https://api.vk.com/method/users.get?v=5.23&user_ids={}&access_token=d95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c&fields=home_town'.format(str(user)))
        response = urllib.request.urlopen(req) # да, так тоже можно, не обязательно делать это с with, как в примере выше
        print(user)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        if 'home_town' not in (data['response'][0]):
            continue
        cities.append(data['response'][0]['home_town'])
        i += 1
    print(len(cities))
    cities = [city for city in cities if city != '']
    from collections import Counter
    cities = Counter(cities)
    cities = dict(cities)
    cities = {c : cities[c] for c in cities if cities[c] > 2 and len(c) > 2}
    print(cities)


def find_smth():
    request = 'https://api.vk.com/method/wall.get?v=5.74&owner_id=-57354358&access_token=d95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c&offset='
    access_token = '&' + 'd95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c'
    arr = []
    for i in range(0, 1001, 100):
        print(i)
        resp = get_page('https://api.vk.com/method/wall.get?v=5.74&owner_id=-57354358&access_token=d95f88c4d95f88c4d95f88c42dd93da4f6dd95fd95f88c4839e41b0a40c5ad5dfed7c1c&offset='+str(i))
        arr.append(resp)
    return arr


def main():
    arr = find_smth()
    print(arr)
    arr_texts = []
    for i in arr['response']['items'][]



if __name__ == "__main__":
    main()
