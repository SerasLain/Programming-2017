import sqlite3

def add_row(c):
    city = str(input('Введите место: '))
    text = str(input('Введите текст: '))
    informant = str(input('Введите имя информанта: '))
    c.execute("INSERT INTO Тексты (city, text, informant) VALUES (?, ?, ?)", [city, text, informant])

conn = sqlite3.connect(r'C:\Users\1\Programming-2017\database.sqlite')
c = conn.cursor()
add_row(c)
conn.commit() ##Сохраняет изменения

