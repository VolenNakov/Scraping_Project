#Initial coomit
import requests
from bs4 import BeautifulSoup as bs

URL = 'https://btvnovinite.bg/'
page = requests.get(URL)

soup = bs(page.content, 'html.parser')
results = soup.find(id='content_router')
news_elems = results.find_all('li', class_='item')
for news_elem in news_elems:
    title_elem = news_elem.find('div', class_='title')
    link_elem = news_elem.find('a', class_='link')
    img_elem = news_elem.find('img', src_='src')
    text_elem = news_elem.find('div', class_='text')
    print(title_elem)
    print(link_elem)
    print(img_elem)
    print(text_elem)
    print()
