from flask import Flask, render_template,request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        conn = get_db_connection()
        conn.execute('INSERT INTO recipes (name, ingredients, instructions) VALUES (?, ?, ?)',
                     (name, ingredients, instructions))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

@app.route('/recipe/<int:id>')
def recipe(id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()
    conn.close()
    if recipe is None:
        return redirect('/')
    return render_template('recipe.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)
