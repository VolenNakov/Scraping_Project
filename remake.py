import requests
import sqlite3
import uuid
import datetime
from bs4 import BeautifulSoup as bs

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
    year = time[13:17]
    month = time[10:12]
    day = time[7:9]
    hour = time[0:2]
    minute = time[3:5]
    return year + "-" + month + "-" + day + " " + hour + ":" + minute + ":00"


def getArticles():
    page = requests.get(URL)
    soup = bs(page.content, "html.parser")
    results = soup.find(class_="list-wrapper")

    articles = results.find_all("li", class_="item")
    for article in articles:
        title = article.find("div", class_="title").text
        link = article.find("a", class_="link")["href"]
        img = article.find("img")["src"]
        id_ = uuid.uuid3(uuid.NAMESPACE_URL, URL + link)
        if str(id_) not in ids:
            for data in [(str(id_), str(title), str(link), str(img))]:
                cur.execute("INSERT INTO news VALUES (?,?,?,?)", data)
                con.commit()
        else:
            print(
                "This article already exists:"
                + "\n    - "
                + str(id_)
                + "\n    - "
                + str(title)
            )


def scrapeArticle(link):
    page = requests.get(URL + link)
    soup = bs(page.text, "html.parser")
    body = soup.find(class_="article-body")
    text = ""
    for tag in body:
        if tag.name == "p":
            text += tag.text + "\n"
    text = text.replace(u"\xa0", u" ")
    data = (str(text),str(uuid.uuid3(uuid.NAMESPACE_URL, URL + link)))
    cur.execute("UPDATE news SET text = ? WHERE id= ?",data)
    con.commit()

def main():
    getArticles()
    link = "/bulgaria/novozarazenite-s-indijskija-variant-na-covid-19-rabotjat-v-stolichnija-gradski-transport.html"
    scrapeArticle(link)


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
