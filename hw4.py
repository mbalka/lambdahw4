from flask import Flask, render_template, request, jsonify
import sqlite3

app=Flask(__name__)

connection = sqlite3.connect('database.db')
print('opened db successfully')

connection.execute('CREATE TABLE IF NOT EXISTS movies (name TEXT, genre TEXT, starringActor TEXT, year TEXT)')
print('table created successfully')
connection.close()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/enternew')
def enternew():
    return render_template('movie.html')


@app.route('/movie', methods=['POST'])
def movie():
    connection=sqlite3.connect('database.db')
    cursor=connection.cursor()

    try:
        name=request.form['name']
        genre=request.form['genre']
        starringActor=request.form['starringActor']
        year=request.form['year']
        cursor.execute('INSERT INTO movies (name, genre, starringActor, year) VALUES (?,?,?,?)', (name, genre, starringActor, year))
        connection.commit()
        message='record successfully added'
    except:
        connection.rollback()
        message='error in insert operation'
    finally:
        return render_template('result.html', message=message)
        connection.close()

@app.route('/movies')
def movies():
    connection=sqlite3.connect('database.db')
    cursor=connection.cursor()
    name=(request.args.get('name'),)
    try:
        cursor.execute('SELECT * FROM movies WHERE name=?', name)
        result=jsonify(results=cursor.fetchall())
    except:
        result='search error'
    finally:
        connection.close()
        return result
