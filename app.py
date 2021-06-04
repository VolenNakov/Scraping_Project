import requests
import sqlite3
import uuid
from bs4 import BeautifulSoup as bs

con = sqlite3.connect('news.db')
cur = con.cursor()
URL = 'https://btvnovinite.bg/'

class News_BTV:
    def __init__(self,title,link,img):
        self.title = title
        self.link = link
        self.img = img

def scrapMainPage():
    page = requests.get(URL)
    
    soup = bs(page.content, 'html.parser')
    results = soup.find(id='content_router')

    news_elems = results.find_all('li', class_='item')
    for news_elem in news_elems:
        title_elem = news_elem.find('div', class_='title')
        link_elem = news_elem.find('a', class_='link')
        img_elem = news_elem.find('img')
        if title_elem is not None and link_elem is not None and img_elem is not None:
            Object = News_BTV(title_elem.text,link_elem['href'],img_elem['src'])
            addToDb(Object)

def addToDb(element):
    id = uuid.uuid3(uuid.NAMESPACE_URL, "https://btvnovinite.bg/"+element.link)
    if cur.execute("SELECT EXISTS(SELECT 1 from news WHERE id='"+str(id)+"')").fetchone():
        print("This Id exsists: "+str(id))
    else:
        for data in [(str(id),str(element.title),str(element.link),str(element.img))]:
            print(id)
            cur.execute('INSERT INTO news VALUES (?,?,?,?)',data)
            con.commit()

def main():
    scrapMainPage()

if __name__ == "__main__":
    main()
