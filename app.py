from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# データベースの初期化
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, quantity INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, type TEXT, quantity INTEGER, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# 商品を追加する関数
def add_product(name, quantity):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO products (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()
    conn.close()

# 入出庫履歴を追加する関数
def add_inventory_history(product_id, type, quantity):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO inventory_history (product_id, type, quantity) VALUES (?, ?, ?)", (product_id, type, quantity))
    conn.commit()
    conn.close()

# 商品登録ページのルート
@app.route('/add_product', methods=['GET', 'POST'])
def add_product_page():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        add_product(name, quantity)
        return redirect(url_for('inventory'))
    return render_template('add_product.html')

# 入出庫履歴登録ページのルート
@app.route('/add_inventory_history', methods=['POST'])
def add_inventory_history_page():
    product_id = request.form['product_id']
    type = request.form['type']
    quantity = request.form['quantity']
    add_inventory_history(product_id, type, quantity)
    return redirect(url_for('inventory'))

# 在庫一覧ページ
@app.route('/inventory')
def inventory():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()

    # 入出庫履歴を取得
    c.execute("SELECT * FROM inventory_history")
    history = c.fetchall()

    conn.close()
    return render_template('inventory.html', products=products, history=history)

# ルートURLにアクセスした際のHTML表示
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home</title>
    </head>
    <body>
        <h1>在庫管理システムへようこそ</h1>
        <p><a href="/add_product">製品の追加</a></p>
        <p><a href="/inventory">在庫を見る</a></p>
    </body>
    </html>
    """

if __name__ == '__main__':
    init_db()  # データベースの初期化
    app.run(debug=True)
