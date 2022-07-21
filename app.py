import email
from unicodedata import name
from flask import Flask, request, redirect, render_template, url_for, redirect
from clear import clear
import sqlite3
import datetime
import random

## Iдеї для оновлень
# особистий кабінет автора + модерація статтей
# Рейтинг статей і авторів (фунція лайку + чарт статтей)


app = Flask(__name__)
database = sqlite3.connect('blog2.db')
cursor = database.cursor()
database.execute('CREATE TABLE IF NOT EXISTS {}(id, title, intro, text, date, user)' .format('data2'))
database.commit()
database.execute('CREATE TABLE IF NOT EXISTS {}(id, quote, author)' .format('data_quotes'))
database.commit()
database.execute('CREATE TABLE IF NOT EXISTS {}(id, name, email, password, date_registration, author_rating)' .format('users'))
database.commit()

@app.route('/')
@app.route('/home')
def index():
    database = sqlite3.connect('blog2.db')
    cursor = database.cursor()
    qoute_id = cursor.execute('SELECT id FROM data_quotes').fetchall()
    random_id = random.randrange(int(clear(qoute_id[0])), int(clear(qoute_id[-1])))
    random_id = str(random_id)
    quote = cursor.execute('SELECT quote FROM data_quotes WHERE id == ?', (random_id,)).fetchone()
    quote = clear(quote)
    author = cursor.execute('SELECT author FROM data_quotes WHERE id == ?', (random_id,)).fetchone()
    author = clear(author)
    quotes = [quote, author]
    return render_template('index.html', quotes=quotes)



@app.route('/about')
def about():
    return render_template('about.html')




@app.route('/user')
def user():
    database = sqlite3.connect('blog2.db')
    cursor = database.cursor()
    qoute_id = cursor.execute('SELECT id FROM data_quotes').fetchall()
    random_id = random.randrange(int(clear(qoute_id[0])), int(clear(qoute_id[-1])))
    random_id = str(random_id)
    quote = cursor.execute('SELECT quote FROM data_quotes WHERE id == ?', (random_id,)).fetchone()
    quote = clear(quote)
    author = cursor.execute('SELECT author FROM data_quotes WHERE id == ?', (random_id,)).fetchone()
    author = clear(author)
    quotes = [quote, author]
    return render_template('user.html', quotes=quotes)


@app.route('/posts')
def posts():
    database = sqlite3.connect('blog2.db')
    cursor = database.cursor()
    art_title = cursor.execute('SELECT title FROM data2').fetchall()
    art_intro = cursor.execute('SELECT intro FROM data2').fetchall()
    art_time = cursor.execute('SELECT date FROM data2').fetchall()
    art_id = cursor.execute('SELECT id FROM data2').fetchall()
    article = []
    for i in range(len(art_title)-1, -1, -1):
        box = []
        box.append(art_title[i])
        box.append(art_intro[i])
        box.append(art_time[i])
        id = str(art_id[i])
        page_id = ''
        for i in id:
            if i != '(':
                if i != ')':
                    if i != ',':
                        if i != "'":
                            if i != '"':
                                page_id += i
        box.append(page_id)
        article.append(box)
    return render_template('posts.html', article=article)   



@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        database = sqlite3.connect('blog2.db')
        cursor = database.cursor()
        art_id = cursor.execute('SELECT id FROM data2').fetchall()
        if len(art_id) != 0:
            id = str(art_id[-1])
            new_id = ''
            for i in id:
                if i != '(':
                    if i != ')':
                        if i != ',':
                            if i != "'":
                                if i != '"':
                                    new_id += i 
            id = str(int(new_id)+1)       
        else:
            id = '0'
        
        
        user = 'test_name'
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        time = []
        a = str(datetime.datetime.now())
        for i in range(16):
            time.append(a[i])
        date = ''
        for i in time:
            date += i

        artitle = [title, intro, time, text]
       
        cursor.execute('INSERT INTO data2 VALUES(?, ?, ?, ?, ?, ?)', (id, title, intro, text, date, user))
        database.commit()
        return render_template('post.html', artitle=artitle)
        
    else:
        return render_template('create-article.html')


@app.route('/posts/<string:id>')
def post(id):
    database = sqlite3.connect('blog2.db')
    cursor = database.cursor()
    art_title = cursor.execute('SELECT title FROM data2 WHERE id == ?', (id,)).fetchone()
    art_title = clear(art_title)
    art_intro = cursor.execute('SELECT intro FROM data2 WHERE id == ?', (id,)).fetchone()
    art_intro = clear(art_intro)
    art_time = cursor.execute('SELECT date FROM data2 WHERE id == ?', (id,)).fetchone()
    art_time = clear(art_time)
    art_text = cursor.execute('SELECT text FROM data2 WHERE id == ?', (id,)).fetchone()
    art_text = clear(art_text)
    artitle = [art_title, art_intro, art_time, art_text]
    return render_template('post.html', artitle=artitle)   


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":
        database = sqlite3.connect('blog2.db')
        cursor = database.cursor()
    
        id = 'test_id'
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        date_registration = 'test_date_registration'
        author_rating = 'test_author_rating'
        user = [name, email, password]
        cursor.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)', (id, name, email, password, date_registration, author_rating))
        database.commit()
   
        return render_template('registration.html', user=user)

    else:
        return render_template('registration.html')





if __name__ == "__main__":
    app.run(debug=False)

