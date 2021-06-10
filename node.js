const express = require('express')
const app = express()
const port = 3000
const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('news.db', sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log('Connected databse')
});

class Article {
  constructor(href, title) {
    this.href = href;
    this.title = title;
  }
}


function createList(array) {
  db.serialize(() => {
    db.each('SELECT href as href, title as title FROM news', (err, row) => {
      if (err) {
        console.error(err);
      }
      else {
        array.push(new Article(row.href, row.title))
      }
    });
  })
};
app.get('/', (req, res) => {
  let html = "";
  let articles = []
  createList(articles)
  console.log(articles)
  for (let i = 0; i < articles.length; i++) {
    html += '<p><a href="' + articles[i].href + '">' + articles[i].title + '</a><br>'
  };
  res.send(html)
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
});

