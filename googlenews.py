"""
С сайта google news (https://news.google.com) (язык и регион - English | United States) прокачиваются все статьи 
за последний месяц (на момент прокачки) с ключевым словом Russia.
Затем для скачанных статей на основе топ-50 наиболее частотных слов создается word cloud.
"""

from datetime import datetime, timedelta
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import urllib
import os
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import re
import numpy as np

#Обработка запроса на ресурс "google-news(en|us)" с ключевым словом Russia
news_url="https://news.google.com/search?q=russia&hl=en-US&gl=US&ceid=US%3Aen"
news_open = urlopen(news_url)
news_soup = soup(news_open, "lxml")
news_list = news_soup.findAll(["h3", "h4"])
dateList_raw = news_soup.findAll("time", {"class": "WW6dff"})

#Получение списка внутренних (внутри google) ссылок на новостии и списка дат публикации каждой новости
linksList = []
dateList = []
for i in range(len(news_list)):
    linksList.append(re.sub('\.', 'https://news.google.com', news_list[i].a['href']))
    dateList.append(datetime.fromtimestamp(int(re.sub(r'seconds: ', '', dateList_raw[i]["datetime"]))))

#Удаление внутренних ссылок на новости, опубликованные ранее последних 30 дней 
d = datetime.today() - timedelta(days = 30)
linksListReduced = np.array(linksList)[np.array(dateList)>d]

#Функция создания внешней ссылки из внутренней
def outerLink_gen(i):
    innerLink = linksListReduced[i]
    innerLink_open = urlopen(innerLink)
    innerLink_soup = soup(innerLink_open, "lxml")
    outerLink = (innerLink_soup.find("noscript")).a['href']
    return outerLink

#Создание пустого списка для внешних ссылок
outerLinksList = []
#Заполнение списка внешними ссылками
print(len(linksListReduced))
for i in range(len(linksListReduced)):
    print(i)
    outerLink = outerLink_gen(i)
    print(outerLink)
    outerLinksList.append(outerLink)

#Функция для извлечения "чистого" текста из новостного ресурса
def processText(webpage):
    #Пустой list для хранения обработанного текста
    processed_text = []
    try:
        news_open = urlopen(webpage)
        news_soup = soup(news_open, "lxml")
        news_para = news_soup.find_all("p", text = True)
        for item in news_para:
            #разделение и объединение слов, чтобы убрать лишние пробелы
            para_text = (' ').join((item.text).split())
            # объединение строк/абзацев в list
            processed_text.append(para_text)
    except (urllib.error.HTTPError, urllib.error.URLError):
        pass
    return processed_text

#Извлечение текста по кажой новостной ссылке и объединение всех новостей в один текст 
text = ''
i = 0
for link in outerLinksList:
    i += 1
    print(i,)
    news_list = processText(link)
    text += (' ').join(news_list)

#Функция нормализации текста и удаления слов, состоящих менее чем из 3 букв. 
def normWords(text, lenWords = 2):
    listOfWords = re.split(r'\W+', text)
    listOfWordsReduced = [wor.lower() for wor in listOfWords if len(wor) > lenWords]
    return listOfWordsReduced

words = normWords(text)

#Построение и сохранение word cloud с помощью готовой библиотеки
currdir = os.path.dirname(__file__)
stopwrds = STOPWORDS
stopwrds.add('will')
def create_wordcloud(text):
    #cloudmask = array(Image.open(os.path.join(currdir, 'cloud.png'))) 
    wordcloud =  WordCloud(max_words = 50,
		    background_color = 'white',
                    stopwords = stopwrds,)
                    #mask = cloudmask)
    wordcloud.generate(text)
    wordcloud.to_file(os.path.join(currdir,'wordcloud.png'))

create_wordcloud((' ').join(words))

#Результат выполнения программы: файл Repository1/wordcloud.png

