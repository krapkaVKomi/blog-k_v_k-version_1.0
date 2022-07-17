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


@app.route('/posts')
def posts():
    return render_template('posts.html')


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
        return render_template('posts.html')
    else:
        return render_template('create-article.html')



if __name__ == "__main__":
    app.run(debug=False)
