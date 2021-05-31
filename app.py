import requests
from bs4 import BeautifulSoup as bs

class News_BTV:
    def __init__(self,title,link,img):
        self.title = title
        self.link = link
        self.img = img

URL = 'https://btvnovinite.bg/'
page = requests.get(URL)

soup = bs(page.content, 'html.parser')
results = soup.find(id='content_router')

news_elems = results.find_all('li', class_='item')
news_list = []

for news_elem in news_elems:
    title_elem = news_elem.find('div', class_='title')
    link_elem = news_elem.find('a', class_='link')
    img_elem = news_elem.find('img')
    news_list.append(News_BTV(title_elem,link_elem,img_elem))
