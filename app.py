from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        image TEXT,
        category_id INTEGER,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')

    # Insert default categories if they don't exist
    cursor.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", ("Seeds", "High-quality seeds for various crops"))
    cursor.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", ("Fertilizers", "Organic and chemical fertilizers"))
    cursor.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", ("Pesticides", "Pest control solutions"))
    cursor.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", ("Tools", "Farming tools and equipment"))
    cursor.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", ("Machinery", "Agricultural machinery"))

    conn.commit()
    conn.close()

# ---------- HOME ----------
@app.route('/')
def home():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Get all categories
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    # Get products by category
    products_by_category = {}
    for category in categories:
        cursor.execute("""
            SELECT p.*, c.name as category_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.category_id = ?
        """, (category[0],))
        products_by_category[category[1]] = cursor.fetchall()

    conn.close()
    return render_template("index.html", products_by_category=products_by_category, categories=categories)

# ---------- REGISTER ----------
@app.route('/register', methods=["GET","POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            
            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username=?",(username,))
            if cursor.fetchone():
                error = "Username already exists!"
            else:
                hashed_password = generate_password_hash(password)
                cursor.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,hashed_password))
                conn.commit()
                conn.close()
                return redirect(url_for("login"))
        except Exception as e:
            error = f"Registration error: {e}"
        finally:
            if conn:
                conn.close()
    return render_template("register.html", error=error)

# ---------- LOGIN ----------
@app.route('/login', methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?",(username,))
            user = cursor.fetchone()
            conn.close()

            if user and check_password_hash(user[2], password):
                session["user"] = username
                session["cart"] = []
                session.modified = True
                return redirect(url_for("home"))
            else:
                error = "Invalid username or password"
        except Exception as e:
            error = f"Login error: {e}"
    return render_template("login.html", error=error)

# ---------- ADD TO CART ----------
@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if "cart" not in session:
        session["cart"] = []
    session["cart"].append(id)
    session.modified = True
    return redirect(url_for("home"))

# ---------- VIEW CART ----------
@app.route('/cart')
def cart():
    cart_items = []
    if "cart" in session:
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            for pid in session["cart"]:
                cursor.execute("SELECT * FROM products WHERE id=?",(pid,))
                cart_items.append(cursor.fetchone())
            conn.close()
        except Exception as e:
            print(f"Cart error: {e}")
    return render_template("cart.html", cart_items=cart_items)

# ---------- REMOVE FROM CART ----------
@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    if "cart" in session and index < len(session["cart"]):
        session["cart"].pop(index)
        session.modified = True
    return redirect(url_for("cart"))

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

# ---------- ADMIN ----------
@app.route('/admin', methods=["GET","POST"])
def admin():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    conn.close()

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        image = request.form["image"]
        category_id = request.form["category_id"]
        description = request.form.get("description", "")

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name,price,image,category_id,description) VALUES (?,?,?,?,?)",
                         (name,price,image,category_id,description))
            conn.commit()
            conn.close()
            return redirect(url_for("admin"))
        except Exception as e:
            print(f"Admin error: {e}")

    return render_template("admin.html", categories=categories)

# ---------- ADD SAMPLE PRODUCTS ----------
def add_sample_products():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Check if products already exist
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    sample_products = [
        # Seeds
        ("Tomato Seeds", 150, "https://images.unsplash.com/photo-1592150621744-aca64f48394a?w=400", 1, "High-quality hybrid tomato seeds, disease resistant"),
        ("Wheat Seeds", 200, "https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=400", 1, "Premium quality wheat seeds for better yield"),
        ("Rice Seeds", 180, "https://images.unsplash.com/photo-1536304993881-ff6e9aefacd?w=400", 1, "Long grain rice seeds, high germination rate"),

        # Fertilizers
        ("NPK Fertilizer 20-20-20", 450, "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=400", 2, "Balanced NPK fertilizer for all crops"),
        ("Organic Manure", 300, "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400", 2, "100% organic manure, improves soil health"),
        ("Urea Fertilizer", 250, "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400", 2, "Nitrogen-rich fertilizer for leafy vegetables"),

        # Pesticides
        ("Insecticide Spray", 350, "https://images.unsplash.com/photo-1585435557343-3b092031e2bb?w=400", 3, "Effective against common garden pests"),
        ("Fungicide Powder", 280, "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", 3, "Controls fungal diseases in plants"),
        ("Herbicide Solution", 420, "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400", 3, "Selective weed control solution"),

        # Tools
        ("Garden Hoe", 180, "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400", 4, "Sturdy garden hoe for soil cultivation"),
        ("Watering Can", 120, "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400", 4, "5-liter capacity watering can"),
        ("Pruning Shears", 250, "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=400", 4, "Professional pruning shears"),

        # Machinery
        ("Hand Tractor", 15000, "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400", 5, "Mini hand tractor for small farms"),
        ("Sprayer Pump", 850, "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400", 5, "Battery operated sprayer pump"),
        ("Seed Drill", 2200, "https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=400", 5, "Manual seed drill for precise planting")
    ]

    for product in sample_products:
        cursor.execute("""
            INSERT INTO products (name, price, image, category_id, description)
            VALUES (?, ?, ?, ?, ?)
        """, product)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    add_sample_products()
    app.run(debug=True)
