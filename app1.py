from bs4.element import ResultSet
import requests
import sqlite3
import uuid
from bs4 import BeautifulSoup as bs

con = sqlite3.connect('news.db')
cur = con.cursor()
URL = 'https://btvnovinite.bg'

ids = []
cur.execute("SELECT * FROM news")
records=cur.fetchall()
for row in records:
    ids.append(row[0])

def mainPage():
    page = requests.get(URL)
    soup = bs(page.content, 'html.parser')
    results = soup.find(class_='list-wrapper')

    elements = results.find_all('li',class_='item')

    for element in elements:
        title = element.find('div',class_='title').text
        link = element.find('a', class_='link')['href']
        img = element.find('img')['src']
        if title is not None and link is not None and img is not None:
            id = uuid.uuid3(uuid.NAMESPACE_URL,URL+link)
            if str(id) not in ids:
                for data in [(str(id),str(title),str(link),str(img))]:
                    cur.execute('INSERT INTO news VALUES (?,?,?,?)',data)
                    con.commit()
            else:
                print("Id already exists - "+str(id))
                
def main():
    mainPage()

if __name__ == "__main__":
    main()                        
