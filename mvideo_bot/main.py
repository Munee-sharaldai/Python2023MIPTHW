import sqlite3
from parsing import scrape_mvideo_data
from logic import create_telegram_bot

url = "https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205?f_category=iphone-914&f_skidka=da&f_tolko-v-nalichii=da&f_seriya-iphone=iphone-15"

data = scrape_mvideo_data(url)
lengths = set(len(lst) for lst in data)
new_data = []
if len(lengths) != 1:
    print("Ошибка: Вложенные списки имеют разную длину.")
else:

    for i in range(len(data[0])):
        new_element = [
            data[0][i],  # iPhone
            data[1][i],  # Цена
            data[2][i],  # Ссылка
            data[3][i],  # Размер
            data[4][i],  # Тип экрана
            data[5][i]   # Процессор
        ]
        new_data.append(new_element)

    for item in new_data:
        print(item)
conn = sqlite3.connect("data.db")

cur = conn.cursor()

cur.executemany("INSERT INTO iphone VALUES (?, ?, ?, ?, ?, ?)", new_data)
conn.commit()
conn.close()

key = '6653192109:AAGhBzBiP8RB0M3wLS3BX4YHY6l18vfzdhw'
create_telegram_bot(key, data)
