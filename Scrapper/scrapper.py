import requests
from bs4 import BeautifulSoup

url = 'https://www.hindustantimes.com/'
page = requests.get(url)
page = page.content

soup = BeautifulSoup(page, 'html.parser')

# list of all the classes which contain headlines
headline_class_list = ['big-story-h2', 'big-story-mid-h3', 'subhead4', 'subhead4 pt-10', 'top-thumb-rgt',
                       'media-heading heading4', 'headingfour', 'media-heading headingfive', 'headingfive',
                       'random-heading', 'para-txt']
headline_div_class = soup.find_all('div', attrs={'class': [headline_class_list]})

# getting text
list_of_news = []
for i in headline_div_class:
    list_of_news.append(i.get_text())
import re

for i in range(len(list_of_news)):
    list_of_news[i] = re.sub('\s+', ' ', list_of_news[i])

# removing small sentences which are not headlines like  select city, know more etc.
fliterlized_news = []
for i in range(len(list_of_news)):
    z = list_of_news[i].split()
    if (len(z) >= 4):
        fliterlized_news.append(list_of_news[i])

# translating Punjabi to English
import langdetect
from translate import Translator

for i in range(len(fliterlized_news)):
    if (langdetect.detect(fliterlized_news[i]) == 'pa'):
        translator = Translator(from_lang='pa', to_lang='en')
        fliterlized_news[i] = translator.translate(fliterlized_news[i])

# writing the headlines row-wise
import csv

with open('today\'s headline.csv', 'w', newline='') as f:
    wr = csv.writer(f)
    for i in fliterlized_news:
        wr.writerow([i])