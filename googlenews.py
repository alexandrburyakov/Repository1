from bs4 import BeautifulSoup as soup
import urllib
from urllib.request import urlopen
import os
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
#from numpy import *

#Обработка запроса на ресурс "google-news(en|us)" с ключевым словом Russia
#для полученя списка ссылок на новости
news_url="https://news.google.com/news/rss/search/section/q/russia?ned=us&gl=US&hl=en"
Client=urlopen(news_url)
xml_page=Client.read()
Client.close()

soup_page=soup(xml_page,"xml")
news_list=soup_page.findAll("item")

#Пустой лист для сохранения списка ссылок на новости
link_list = []
for news in news_list:
    #Сохранение ссылок на новости в список
    link_list.append(news.link.text)

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
    except urllib.error.HTTPError:
        pass
    return processed_text

#Извлечение текста по кажой новостной ссылке и объединение всех новостей в один текст 
text = ''
i = 0
for link in link_list:
    i += 1
    print(i,)
    news_list = processText(link)
    text += (' ').join(news_list)

#Построение и сохранение word cloud с помощью готовой библиотеки
currdir = os.path.dirname(__file__)
stopwrds = STOPWORDS
stopwrds.add('will')
def create_wordcloud(text):
    #cloudmask = array(Image.open(os.path.join(currdir, 'cloud.png'))) 
    wc =  WordCloud(max_words = 50,
		    background_color = 'white',
                    stopwords = stopwrds,)
                    #mask = cloudmask)
    wc.generate(text)
    wc.to_file(os.path.join(currdir,'wc.png'))

create_wordcloud(text) 



