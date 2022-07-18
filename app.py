from flask import Flask, request, redirect, render_template, url_for, redirect
import sqlite3


app = Flask(__name__)

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
    database = sqlite3.connect('blog.db')
    cursor = database.cursor()
    database.execute('CREATE TABLE IF NOT EXISTS {}(title, intro, text)' .format('data'))
    database.commit()
    art = cursor.execute('SELECT title FROM data').fetchall()
    art1 = cursor.execute('SELECT intro FROM data').fetchall()
    art2 = cursor.execute('SELECT text FROM data').fetchall()
    article = []
    for i in range(len(art)-1, -1, -1):
        box = []
        box.append(art[i])
        box.append(art1[i])
        box.append(art2[i])
        article.append(box)
    return render_template('posts.html', article=article)
    


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        database = sqlite3.connect('blog.db')
        cursor = database.cursor()
        database.execute('CREATE TABLE IF NOT EXISTS {}(title, intro, text)' .format('data'))
        database.commit()
        cursor.execute('INSERT INTO data VALUES(?, ?, ?)', (title, intro, text))
        database.commit()
        return render_template('post.html')
        
    else:
        return render_template('create-article.html')



if __name__ == "__main__":
    app.run(debug=False)
