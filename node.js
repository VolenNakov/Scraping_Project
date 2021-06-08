const express = require('express')
const app = express()
const port = 3000
const sqlite3 = require('sqlite3').verbose();
let html = ""
let db = new sqlite3.Database('news.db', sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log('Connected databse')
});


app.get('/', (req, res) => {
  db.serialize(() => {
    db.each('SELECT href as href,title as title FROM news', (err, row) => {
      if (err) {
        console.error(err.message);
      }
      html+='<p><a href="'+row.href+'">'+row.title+'</a><br>'
    });
  });
  console.log(html)
  res.send(html)
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
});

