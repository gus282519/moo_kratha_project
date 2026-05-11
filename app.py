from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'moo_kratha_project.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute('PRAGMA foreign_keys = ON')
    db.execute('''
        CREATE TABLE IF NOT EXISTS Categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS Meats (
            meat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            meat_name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            price REAL NOT NULL,
            spiciness_level TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES Categories(category_id)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        )
    ''')
    db.commit()
    db.close()


@app.route('/')
def home():
    db = get_db()
    products = db.execute('''
        SELECT p.*, c.category_name AS category_name
        FROM Meats p
        LEFT JOIN Categories c ON p.category_id = c.category_id
        ORDER BY p.meat_id DESC
    ''').fetchall()
    categories = db.execute('SELECT * FROM Categories ORDER BY category_name').fetchall()
    return render_template('index.html', page='home', products=products, categories=categories)


@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    db = get_db()
    categories = db.execute('SELECT * FROM Categories ORDER BY category_name').fetchall()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = request.form.get('price', '0').strip() or '0'
        category_id = request.form.get('category_id')
        description = request.form.get('description', '').strip()
        spiciness_level = request.form.get('spiciness_level', '').strip()
        if name and category_id:
            db.execute(
                'INSERT INTO Meats (meat_name, category_id, price, description, spiciness_level) VALUES (?, ?, ?, ?, ?)',
                (name, int(category_id), float(price), description, spiciness_level)
            )
            db.commit()
            return redirect(url_for('home'))
    return render_template('index.html', page='product_form', categories=categories, action='Add', product=None)


@app.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    db = get_db()
    product = db.execute('SELECT * FROM Meats WHERE meat_id = ?', (product_id,)).fetchone()
    if not product:
        return redirect(url_for('home'))
    categories = db.execute('SELECT * FROM Categories ORDER BY category_name').fetchall()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price = request.form.get('price', '0').strip() or '0'
        category_id = request.form.get('category_id')
        description = request.form.get('description', '').strip()
        spiciness_level = request.form.get('spiciness_level', '').strip()
        if name and category_id:
            db.execute(
                '''UPDATE Meats SET meat_name = ?, category_id = ?, price = ?, description = ?, spiciness_level = ?
                   WHERE meat_id = ?''',
                (name, int(category_id), float(price), description, spiciness_level, product_id)
            )
            db.commit()
            return redirect(url_for('home'))
    return render_template('index.html', page='product_form', categories=categories, action='Edit', product=product)


@app.route('/product/delete/<int:product_id>')
def delete_product(product_id):
    db = get_db()
    db.execute('DELETE FROM Meats WHERE meat_id = ?', (product_id,))
    db.commit()
    return redirect(url_for('home'))


@app.route('/category/add', methods=['GET', 'POST'])
def add_category():
    db = get_db()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if name:
            db.execute('INSERT OR IGNORE INTO Categories (category_name, description) VALUES (?, ?)', (name, description))
            db.commit()
            return redirect(url_for('home'))
    return render_template('index.html', page='category_form', action='Add', category=None)


@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    db = get_db()
    category = db.execute('SELECT * FROM Categories WHERE category_id = ?', (category_id,)).fetchone()
    if not category:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if name:
            db.execute('UPDATE Categories SET category_name = ?, description = ? WHERE category_id = ?', (name, description, category_id))
            db.commit()
            return redirect(url_for('home'))
    return render_template('index.html', page='category_form', action='Edit', category=category)


@app.route('/category/delete/<int:category_id>')
def delete_category(category_id):
    db = get_db()
    db.execute('DELETE FROM Categories WHERE category_id = ?', (category_id,))
    db.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
