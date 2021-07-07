import requests
import sqlite3
import uuid
from bs4 import BeautifulSoup as bs

con = sqlite3.connect('news.db')
cur = con.cursor()
URL = 'https://btvnovinite.bg'

ids = []
cur.execute("SELECT id FROM news")
records = cur.fetchall()
for row in records:
    ids.append(row[0])
def getArticles():
    page = requests.get(URL)
    soup = bs(page.content, 'html.parser')
    results = soup.find(class_='list-wrapper')

    articles = results.find_all('li',class_='item')
    for article in articles:
        title = article.find('div',class_='title').text
        link = article.find('a',class_='link')['href']
        img = article.find('img')['src']
        id_ = uuid.uuid3(uuid.NAMESPACE_URL,URL+link)
        if str(id_) not in ids:
            for data in [(str(id_),str(title),str(link),str(img))]:
                cur.execute('INSERT INTO news VALUES (?,?,?,?)',data)
                con.commit()
        else:
            print('This article already exists:'+'\n    - '+str(id_)+'\n    - '+str(title))
def scrapeArticle(link):
    page = requests.get('https://btvnovinite.bg/bulgaria/novozarazenite-s-indijskija-variant-na-covid-19-rabotjat-v-stolichnija-gradski-transport.html')
    soup = bs(page.text,'html.parser')
    title = soup.find('h1',class_='article-title')
    body = soup.find(class_="article-body")
    print(title.text)
    #title = result.find('h1',class_="article-title")
def main():
    #getArticles()
    link = '/bulgaria/novozarazenite-s-indijskija-variant-na-covid-19-rabotjat-v-stolichnija-gradski-transport.html'
    scrapeArticle(link)
if __name__ == "__main__":
    main()
