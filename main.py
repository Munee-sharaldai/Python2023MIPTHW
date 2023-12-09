# main.py
from db import scrape_mvideo_data
from logic import create_telegram_bot

url = "https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205?f_category=iphone-914&f_skidka=da&f_tolko-v-nalichii=da&f_seriya-iphone=iphone-15"

# Perform web scraping
data = scrape_mvideo_data(url)

# Create and run the Telegram bot
key = '6653192109:AAGhBzBiP8RB0M3wLS3BX4YHY6l18vfzdhw'
create_telegram_bot(key, data)
