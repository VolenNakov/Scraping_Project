const express = require('express')
const app = express()
const port = 3000
const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database('news.db', sqlite3.OPEN_READONLY, (err) => {
  if (err) {
    return console.error(err.message);
  }
  console.log('Connected to database')
});

class Article {
  constructor(href, title) {
    this.href = href;
    this.title = title;
  }
}

app.get('/', (req, res) => {
  let html = "";
	db.all('SELECT id, img_src, title FROM news', (err, articles) => {
		// тук вече имаме данните
		for (let i = 0; i < articles.length; i++) {
			html += '<p><a href="' + articles[i].id + '">' + articles[i].title + '</a><img src='+articles[i].img_src+' width="200" height="100"><br>'
            
		};
		res.send(html)
	});
});
app.get('/:articleid', (req, res) => {
    let html = '';
    console.log(req.params['articleid']);
    res.send(html) 
});
app.get('/favicon.ico', (req, res) => res.status(204));
app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
});
