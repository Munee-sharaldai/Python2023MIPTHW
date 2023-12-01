from bs4 import BeautifulSoup as BS
from selenium import webdriver
import time
import lxml
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import requests
from typing import List
import telebot
import random

#ссылка на бота  = https://t.me/MvideoIphoneBot


url = "https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205?f_category=iphone-914&f_skidka=da&f_tolko-v-nalichii=da&f_seriya-iphone=iphone-15"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(15) #ВОВРЕМЯ ЭТОГО ТАЙМИНГА НЕОБХОДИМО ПРОСКРОЛЛИТЬ ВСЮ СТРАНИЦУ, Т.К. ДАННЫМ ЗАГРУЖАЮТСЯ ДИНАМИЧЕСКИ
html = driver.page_source
soup = BS(html, "lxml")
key = '6653192109:AAGhBzBiP8RB0M3wLS3BX4YHY6l18vfzdhw'

iph_names = soup.find_all("a", "product-title__text")
names = []
for name in iph_names:
    names.append(name)
clear_names2 = [c.text for c in names]
clear_names = [item.replace('Смартфон Apple', '').lstrip(' ').strip(' ') for item in clear_names2]

iph_prices = soup.find_all("span", "price__main-value")
prices = []
for price in iph_prices:
    prices.append(price)
clear_prices = [c.text for c in prices]


iph_descrs = soup.find_all("ul", class_="product-feature-list product-feature-list--undefined")

descrs = []
for descrs_li in iph_descrs:
    iph_1 = descrs_li.find_all("li", class_="product-feature-list__item")
    for descrs_span in iph_1:
        iph_descr = descrs_span.find("span", class_="product-feature-list__value")
        for all_descr in iph_descr:
            descrs.append(all_descr.text)

ul_elements = soup.find_all('ul', class_='product-feature-list--undefined')

screen_list = []
technology_list = []
processor_list = []
camera_list = []

for ul_element in ul_elements:
    li_elements = ul_element.find_all('li', class_='product-feature-list__item--undefined')

    for li_element in li_elements:
        span_name = li_element.find('span', class_='product-feature-list__name')
        span_value = li_element.find('span', class_='product-feature-list__value')

        if span_name and span_value:
            name = span_name.text.strip()
            value = span_value.text.strip()

            if name == 'Экран':
                screen_list.append(value)
            elif name == 'Технология экрана':
                technology_list.append(value)
            elif name == 'Тип процессора':
                processor_list.append(value)
            elif name == 'Основная камера МПикс':
                camera_list.append(value)


print("Список экранов:", screen_list, len(screen_list))
print("Список технологий экрана:", technology_list, len(technology_list))
print("Список типов процессоров:", processor_list, len(processor_list))
print("Список камера:", camera_list, len(camera_list))

soup2 = BS(html, "lxml")
items = soup2.find_all("mvid-plp-product-title", class_="product-card--list__title")
urls = []
for item in items:
    item_url = item.find("div", class_='product-title product-title--list').find("a").get('href')
    urls.append(item_url)
photos = []
block_photo = soup.find_all("img", src_="product-picture__img")
for photo in block_photo:
    photos.append(photo)

print(clear_names)
print("iPhone 15 128GB Blue (Dual Sim)")
#while True:
  #  user_input = input("Введите название товара в данном выше формате(последний параметр может отсутстовать): ")
#
  #  if user_input.lower() == 'exit':
  #      break
#
  #  found = False
  #  for i in range(len(clear_names)):
 #       if user_input.lower() == clear_names[i].lower():
  #          print("Название:", clear_names[i], "|", "Цена:", clear_prices[i], "|", "Ссылка:",
 #                 f"https://www.mvideo.ru{urls[i]}", "|", "Экран:", screen_list[i],"|", "Технология экрана:", technology_list[i],"|", "Тип процессора:", processor_list[i],"|", "Основная камера:", camera_list[i])
  #          found = True
   #         break
#
   # if not found:
   #    print("Товар не найден. Пожалуйста, введите корректное название.")


# Создание бота
bot = telebot.TeleBot(key)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Введите название iPhone для получения информации в данном формате: iPhone 15 128GB Blue (Dual Sim), последний параметр может отсутсвовать.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text

    for i in range(len(clear_names)):
        if user_input.lower() in clear_names[i].lower():
            response_message = (
                f"Название: {clear_names[i]}\n"
                f"Цена: {clear_prices[i]}\n"
                f"Ссылка: https://www.mvideo.ru{urls[i]}\n"
                f"Экран: {screen_list[i]}\n" 
                f"Технология экрана: {technology_list[i]}\n"
                f"Тип процессора: {processor_list[i]}\n"
                f"Основная камера: {camera_list[i]}\n"
            )
            bot.send_message(message.chat.id, response_message)
            return

    bot.send_message(message.chat.id, "Извините, товар не найден.")

bot.polling()

