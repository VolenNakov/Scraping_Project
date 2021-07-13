'use strict';
const express = require('express');
const app = express();
const port = 3000;
const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('news.db', sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    return console.error(err.message);
  };
  console.log('Connected to database');
});

app.get('/', (req, res) => {
  let html = "<div class='text'> ";
  db.all('SELECT news.id, news.img_src, news.href, news.title FROM news INNER JOIN articles ON news.id = articles.id WHERE articles.text != "null"', (err, articles) => {
    // тук вече имаме данните
    for (let i = 0; i < articles.length; i++) {
      html += '<p><a href="' + articles[i].id + '">' + articles[i].title + '</a><img src=' + articles[i].img_src + ' width="200" height="100"><br>';
    };
    html += "</div>"
  });
  db.all('SELECT news.id, news.img_src, news.href, news.title FROM news INNER JOIN articles ON news.id = articles.id WHERE articles.text == "null"',(err,articles)=>{
    html += "<div class='textless'> "
    for (let i = 0; i < articles.length; i++) {
      html += '<p><a href="' + articles[i].id + '">' + articles[i].title + '</a><img src=' + articles[i].img_src + ' width="200" height="100"><br>';
    };
    html += "</div>"
    res.send(html);
  });
});
app.get('/:articleid', (req, res) => {
  let html = '<span style="white-space: pre-line">';
  db.all('SELECT text FROM articles WHERE id = ?', req.params['articleid'], (err, text) => {
    try {
      if (text[0].text) {
        html += text[0].text;
      };
    }
    catch (e) {
      html += "There's nothing here";
    };
    text += '</span>';
    res.send(html);
  });
  console.log(req.params['articleid']);
});

app.get('/favicon.ico', (req, res) => res.status(204));
app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
