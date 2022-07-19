from flask import Flask, request, redirect, render_template, url_for, redirect
import sqlite3
import datetime


app = Flask(__name__)
database = sqlite3.connect('blog2.db')
cursor = database.cursor()
database.execute('CREATE TABLE IF NOT EXISTS {}(id, title, intro, text, date, user)' .format('data2'))
database.commit()


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post')
def post():
    
    return render_template('post.html')


@app.route('/posts')
def posts():
    database = sqlite3.connect('blog2.db')
    cursor = database.cursor()
    art_title = cursor.execute('SELECT title FROM data2').fetchall()
    art_intro = cursor.execute('SELECT intro FROM data2').fetchall()
    art_time = cursor.execute('SELECT date FROM data2').fetchall()
    article = []
    for i in range(len(art_title)-1, -1, -1):
        box = []
        box.append(art_title[i])
        box.append(art_intro[i])
        box.append(art_time[i])
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
            id = int(new_id)+1        
        else:
            id = 0
        
        
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
       
        cursor.execute('INSERT INTO data2 VALUES(?, ?, ?, ?, ?, ?)', (id, title, intro, text, date, user))
        database.commit()
        return render_template('post.html')
        
    else:
        return render_template('create-article.html')

'''
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return "User page: " + name + "-" + str(id)
'''

if __name__ == "__main__":
    app.run(debug=False)
