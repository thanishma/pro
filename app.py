from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'restaurant.db'


def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            menu_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (menu_id) REFERENCES menu (id)
        )
    ''')

    conn.commit()
    conn.close()


def insert_menu_item(name, price):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO menu (name, price) VALUES (?, ?)', (name, price))
    conn.commit()
    conn.close()


def get_all_menu_items():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu')
    menu_items = cursor.fetchall()
    conn.close()
    return menu_items


@app.route('/menu', methods=['GET'])
def get_menu():
    menu_items = get_all_menu_items()
    return jsonify(menu_items)


@app.route('/menu', methods=['POST'])
def add_menu_item():
    name = request.json['name']
    price = request.json['price']
    insert_menu_item(name, price)
    return jsonify({'message': 'Menu item added successfully'}), 201


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0')
