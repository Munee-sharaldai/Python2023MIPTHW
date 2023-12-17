import sqlite3
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
from webdriver_manager.chrome import ChromeDriverManager
import requests
from typing import List
import telebot
import random

def scrape_mvideo_data(url):
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service()
    driver = webdriver.Chrome(service=service, options=opts)
    driver.get(url)
    time.sleep(15)
    html = driver.page_source
    soup = BS(html, "lxml")

    args = []
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

    soup2 = BS(html, "lxml")
    items = soup2.find_all("mvid-plp-product-title", class_="product-card--list__title")
    urls = []
    for item in items:
        item_url = item.find("div", class_='product-title product-title--list').find("a").get('href')
        urls.append(item_url)

    return clear_names, clear_prices, urls, screen_list, technology_list, processor_list
