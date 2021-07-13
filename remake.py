import requests
import sqlite3
import uuid
from datetime import datetime
from bs4 import BeautifulSoup as bs

debug = False
con = sqlite3.connect("news.db")
cur = con.cursor()
URL = "https://btvnovinite.bg"

ids = []
cur.execute("SELECT id FROM news")
records = cur.fetchall()
for row in records:
    ids.append(row[0])


def convertTime(time):
    time = time.replace("ч.", "").replace("г.", "")
    year, month, day, hour, minute = time[13:17], time[10:12], time[7:9], time[0:2], time[3:5]
    return year + "-" + month + "-" + day + " " + hour + ":" + minute + ":00"


def getArticles():
    page = requests.get(URL)
    soup = bs(page.content, "html.parser")
    results = soup.find(class_="list-wrapper")

    articles = results.find_all("li", class_="item")
    
    for article in articles:
        title, link, img= article.find("div", class_="title").text, article.find("a", class_="link")["href"], article.find("img")["src"]
        id_ = uuid.uuid3(uuid.NAMESPACE_URL, URL + link)
        if str(id_) not in ids:
            for data in [(str(id_), str(title), str(link), str(img))]:
                cur.execute("INSERT INTO news VALUES (?,?,?,?)", data)
                con.commit()
            cur.execute("INSERT INTO articles VALUES (?,?,?,?)",
                        (str(id_), "NULL", "NULL","NULL"))
            con.commit()
        else:
            if debug:
                print(
                    "This article already exists:"
                    + "\n    - "
                    + str(id_)
                    + "\n    - "
                    + str(title)
                )


def scrapeArticle(link):
    page = requests.get(URL + link)
    if page.url == URL:
        if debug:
            print("This article is deleted - "+link)
    else:
        soup = bs(page.text, "html.parser")
        try:
            modified, tags = soup.find("span", class_="modified"), [tag.text for tag in soup.find(class_='keywords-wrapper').findAll('a')]
        except AttributeError:
            tags = "None"
        id_ = str(uuid.uuid3(uuid.NAMESPACE_URL, URL + link))
        check = cur.execute(
            '''SELECT modified FROM articles WHERE id = ?''', (id_,)).fetchall()
        if check[0][0] == 'NULL':
            body = soup.find(class_="article-body")
            text = ' '.join(map(str,[tag.text + '\n' for tag in body if tag.name == 'p']))
            cur.execute('''UPDATE articles SET modified = ?, text = ? WHERE id =?''',
                        (convertTime(modified.text), text, id_))
            con.commit()
        elif datetime.strptime(check[0][0], "%Y-%m-%d %H:%M:%S") < datetime.strptime(convertTime(modified.text), "%Y-%m-%d %H:%M:%S"):
            body = soup.find(class_="article-body")
            print("This is changed -"+link+id_)
            print(' '.join(map(str,[tag.text + '\n' for tag in body if tag.name == 'p'])))
            #cur.execute('''UPDATE articles SET modified = ? WHER id = ?''',(convertTime(modified.text),id_))
            # con.commit(0)


def main():
    getArticles()
    cur.execute('SELECT href FROM news')
    links = cur.fetchall()
    for link in links:
        scrapeArticle(link[0])


if __name__ == "__main__":
    main()

# title = soup.find("h1", class_="article-title")
    # summary = soup.find(class_="article-summary")
    # published = soup.find("span", class_="published")
    # modified = soup.find("span", class_="modified")
    # if tag.name == "div" and tag["class"] == ["embedded", "link"]:
    #         tag.find("img")["src"]
    #         tag.find("a")["href"]
    #         tag.find("a").text
