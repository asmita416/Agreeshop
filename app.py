from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "secretkey"

# ---------- LANGUAGE/LOCALIZATION ----------
SUPPORTED_LANGUAGES = ['en', 'hi', 'mr']
translations = {}

def load_translations():
    """Load all translation files"""
    global translations
    for lang in SUPPORTED_LANGUAGES:
        try:
            with open(f'translations/{lang}.json', 'r', encoding='utf-8') as f:
                translations[lang] = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Translation file for {lang} not found")
            translations[lang] = {}

def get_locale():
    """Get current language from session, default to English"""
    return session.get('language', 'en')

def get_translation(key, default=''):
    """Get translated string for key"""
    locale = get_locale()
    return translations.get(locale, {}).get(key, translations.get('en', {}).get(key, default))

# Load translations when app starts
load_translations()

@app.before_request
def inject_translations():
    """Make translation function available in all templates"""
    request.get_translation = get_translation
    request.current_language = get_locale()

@app.route('/set_language/<language>')
def set_language(language):
    """Set the user's preferred language"""
    if language in SUPPORTED_LANGUAGES:
        session['language'] = language
    return redirect(request.referrer or url_for('home'))

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        city TEXT,
        pincode TEXT,
        created_at TIMESTAMP,
        role TEXT DEFAULT 'customer'
    )
    ''')

    cursor.execute("PRAGMA table_info(users)")
    user_columns = [row[1] for row in cursor.fetchall()]
    if "role" not in user_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'customer'")

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
        stock INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_id INTEGER,
        added_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        total_amount REAL,
        order_date TIMESTAMP,
        status TEXT,
        payment_status TEXT,
        payment_id TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS delivery (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        status TEXT,
        estimated_date TEXT,
        delivery_date TEXT,
        notes TEXT,
        updated_at TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders (id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        amount REAL,
        payment_method TEXT,
        status TEXT,
        transaction_id TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders (id)
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
    category_products = []
    for category in categories:
        cursor.execute("""
            SELECT p.*, c.name as category_name
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.category_id = ?
        """, (category[0],))
        products = cursor.fetchall()
        category_products.append((category, products))

    conn.close()
    return render_template("index.html", category_products=category_products, categories=categories)

# ---------- CATEGORY VIEW ----------
@app.route('/category/<int:cat_id>')
def view_category(cat_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM categories WHERE id=?", (cat_id,))
    category = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM products WHERE category_id=?
    """, (cat_id,))
    products = cursor.fetchall()

    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    conn.close()
    return render_template("category.html", category=category, products=products, categories=categories)

# ---------- REGISTER ----------
@app.route('/register', defaults={'role': 'customer'}, methods=["GET","POST"])
@app.route('/seller-register', defaults={'role': 'seller'}, methods=["GET","POST"])
def register(role):
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phone = request.form.get("phone", "")
        role = request.form.get("role", role)

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            
            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            if cursor.fetchone():
                error = "Username already exists!"
            else:
                hashed_password = generate_password_hash(password)
                cursor.execute("""INSERT INTO users (username,password,email,phone,created_at,role) 
                               VALUES (?,?,?,?,?,?)""", 
                             (username, hashed_password, email, phone, datetime.now(), role))
                conn.commit()
                conn.close()
                if role == 'seller':
                    return redirect(url_for('login', role='seller'))
                return redirect(url_for("login"))
        except Exception as e:
            error = f"Registration error: {e}"
        finally:
            if conn:
                conn.close()
    return render_template("register.html", error=error, role=role)

# ---------- LOGIN ----------
@app.route('/login', defaults={'role': 'customer'}, methods=["GET","POST"])
@app.route('/seller-login', defaults={'role': 'seller'}, methods=["GET","POST"])
def login(role):
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            user = cursor.fetchone()
            conn.close()

            if user and check_password_hash(user[2], password):
                if user[9] != role:
                    error = f"Please use the {role} login page for this account."
                else:
                    session["user"] = username
                    session["user_role"] = role
                    if role == 'customer':
                        session["cart"] = {}
                    session.modified = True
                    if role == 'seller':
                        return redirect(url_for('seller_dashboard'))
                    return redirect(url_for("home"))
            else:
                if not error:
                    error = "Invalid username or password"
        except Exception as e:
            error = f"Login error: {e}"
    return render_template("login.html", error=error, role=role)

# ---------- ADD TO CART ----------
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = {}
    
    cart = session["cart"]
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    
    session.modified = True
    return redirect(request.referrer or url_for("home"))

# ---------- VIEW CART ----------
@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    
    if "cart" in session and session["cart"]:
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            
            for product_id, quantity in session["cart"].items():
                cursor.execute("SELECT * FROM products WHERE id=?", (int(product_id),))
                product = cursor.fetchone()
                if product:
                    price = float(product[2])  # Convert price to float
                    subtotal = price * quantity
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'subtotal': subtotal
                    })
                    total += subtotal
            
            conn.close()
        except Exception as e:
            print(f"Cart error: {e}")
    
    shipping = 50 if total > 0 else 0
    final_total = total + shipping
    
    return render_template("cart.html", cart_items=cart_items, total=total, shipping=shipping, final_total=final_total)

# ---------- UPDATE CART QUANTITY ----------
@app.route('/update_cart/<int:product_id>/<int:quantity>')
def update_cart(product_id, quantity):
    if "cart" not in session:
        session["cart"] = {}
    
    if quantity <= 0:
        session["cart"].pop(str(product_id), None)
    else:
        session["cart"][str(product_id)] = quantity
    
    session.modified = True
    return redirect(url_for("cart"))

# ---------- REMOVE FROM CART ----------
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if "cart" in session:
        session["cart"].pop(str(product_id), None)
        session.modified = True
    return redirect(url_for("cart"))

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

# ---------- WISHLIST ----------
@app.route('/wishlist')
def wishlist():
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username=?", (session["user"],))
    user = cursor.fetchone()
    
    if user:
        cursor.execute("""
            SELECT p.* FROM products p
            INNER JOIN wishlist w ON p.id = w.product_id
            WHERE w.user_id = ?
            ORDER BY w.added_at DESC
        """, (user[0],))
        wishlist_items = cursor.fetchall()
    else:
        wishlist_items = []
    
    conn.close()
    return render_template("wishlist.html", wishlist_items=wishlist_items)

# ---------- ADD TO WISHLIST ----------
@app.route('/add_to_wishlist/<int:product_id>')
def add_to_wishlist(product_id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username=?", (session["user"],))
    user = cursor.fetchone()
    
    if user:
        cursor.execute("SELECT id FROM wishlist WHERE user_id=? AND product_id=?", (user[0], product_id))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO wishlist (user_id, product_id, added_at)
                VALUES (?, ?, ?)
            """, (user[0], product_id, datetime.now()))
            conn.commit()
    
    conn.close()
    return redirect(request.referrer or url_for("home"))

# ---------- REMOVE FROM WISHLIST ----------
@app.route('/remove_from_wishlist/<int:product_id>')
def remove_from_wishlist(product_id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username=?", (session["user"],))
    user = cursor.fetchone()
    
    if user:
        cursor.execute("DELETE FROM wishlist WHERE user_id=? AND product_id=?", (user[0], product_id))
        conn.commit()
    
    conn.close()
    return redirect(url_for("wishlist"))

# ---------- PROFILE ----------
@app.route('/profile', methods=["GET","POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=?", (session["user"],))
    user = cursor.fetchone()
    
    if request.method == "POST":
        email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        address = request.form.get("address", "")
        city = request.form.get("city", "")
        pincode = request.form.get("pincode", "")
        
        cursor.execute("""
            UPDATE users 
            SET email=?, phone=?, address=?, city=?, pincode=?
            WHERE username=?
        """, (email, phone, address, city, pincode, session["user"]))
        
        conn.commit()
        user = (user[0], user[1], user[2], email, phone, address, city, pincode, user[8], user[9])
    
    conn.close()
    return render_template("profile.html", user=user)

# ---------- CHECKOUT ----------
@app.route('/checkout', methods=["GET","POST"])
def checkout():
    if "user" not in session:
        return redirect(url_for("login"))
    
    if not session.get("cart"):
        return redirect(url_for("cart"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=?", (session["user"],))
    user = cursor.fetchone()
    
    if request.method == "POST":
        # Create order
        total_amount = float(request.form.get("total_amount", 0))
        
        cursor.execute("""
            INSERT INTO orders (user_id, total_amount, order_date, status, payment_status)
            VALUES (?, ?, ?, ?, ?)
        """, (user[0], total_amount, datetime.now(), "Pending", "Pending"))
        
        order_id = cursor.lastrowid
        
        # Add order items
        for product_id, quantity in session["cart"].items():
            cursor.execute("SELECT price FROM products WHERE id=?", (int(product_id),))
            product = cursor.fetchone()
            
            if product:
                cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                """, (order_id, int(product_id), quantity, product[0]))
        
        # Create delivery record
        cursor.execute("""
            INSERT INTO delivery (order_id, status, estimated_date, updated_at)
            VALUES (?, ?, ?, ?)
        """, (order_id, "Processing", "3-5 business days", datetime.now()))
        
        conn.commit()
        session["order_id"] = order_id
        session["cart"] = {}
        session.modified = True
        
        conn.close()
        return redirect(url_for("payment", order_id=order_id))
    
    # Calculate cart total
    cart_items = []
    total = 0
    
    if "cart" in session and session["cart"]:
        for product_id, quantity in session["cart"].items():
            cursor.execute("SELECT * FROM products WHERE id=?", (int(product_id),))
            product = cursor.fetchone()
            if product:
                price = float(product[2])  # Convert price to float
                subtotal = price * quantity
                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
                total += subtotal
    
    shipping = 50
    final_total = total + shipping
    
    conn.close()
    
    return render_template("checkout.html", user=user, cart_items=cart_items, 
                         total=total, shipping=shipping, final_total=final_total)

# ---------- PAYMENT PAGE ----------
@app.route('/payment/<int:order_id>', methods=["GET","POST"])
def payment(order_id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    order = cursor.fetchone()
    
    if request.method == "POST":
        payment_method = request.form.get("payment_method", "online")
        
        # For demo, mark payment as successful
        cursor.execute("""
            UPDATE orders 
            SET payment_status=?
            WHERE id=?
        """, ("Completed", order_id))
        
        cursor.execute("""
            INSERT INTO payments (order_id, amount, payment_method, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (order_id, order[2], payment_method, "Completed", datetime.now()))
        
        cursor.execute("""
            UPDATE orders 
            SET status=?
            WHERE id=?
        """, ("Confirmed", order_id))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for("order_confirmation", order_id=order_id))
    
    conn.close()
    return render_template("payment.html", order=order)

# ---------- ORDER CONFIRMATION ----------
@app.route('/order-confirmation/<int:order_id>')
def order_confirmation(order_id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    order = cursor.fetchone()
    
    cursor.execute("""
        SELECT oi.*, p.name FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id=?
    """, (order_id,))
    order_items = cursor.fetchall()
    
    cursor.execute("SELECT * FROM delivery WHERE order_id=?", (order_id,))
    delivery = cursor.fetchone()
    
    conn.close()
    
    return render_template("order_confirmation.html", order=order, order_items=order_items, delivery=delivery)

# ---------- ORDER TRACKING ----------
@app.route('/my-orders')
def my_orders():
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE username=?", (session["user"],))
    user = cursor.fetchone()
    
    cursor.execute("""
        SELECT * FROM orders WHERE user_id=?
        ORDER BY order_date DESC
    """, (user[0],))
    orders = cursor.fetchall()
    
    conn.close()
    
    return render_template("my_orders.html", orders=orders)

# ---------- ORDER DETAILS ----------
@app.route('/order/<int:order_id>')
def order_details(order_id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    order = cursor.fetchone()
    
    cursor.execute("""
        SELECT oi.*, p.name, p.image FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id=?
    """, (order_id,))
    order_items = cursor.fetchall()
    
    cursor.execute("SELECT * FROM delivery WHERE order_id=?", (order_id,))
    delivery = cursor.fetchone()
    
    conn.close()
    
    return render_template("order_details.html", order=order, order_items=order_items, delivery=delivery)

# ---------- CANCEL ORDER ----------
@app.route('/cancel_order/<int:order_id>')
def cancel_order(order_id):
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE username=?", (session["user"],))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return redirect(url_for("login"))

    cursor.execute("SELECT user_id, status FROM orders WHERE id=?", (order_id,))
    order = cursor.fetchone()
    if not order or order[0] != user[0]:
        conn.close()
        return redirect(url_for("my_orders"))

    if order[1] not in ["Shipped", "Delivered", "Cancelled"]:
        cursor.execute("UPDATE orders SET status=?, payment_status=? WHERE id=?", ("Cancelled", "Cancelled", order_id))
        cursor.execute("UPDATE delivery SET status=?, notes=?, updated_at=? WHERE order_id=?", ("Cancelled", "Order cancelled by customer", datetime.now(), order_id))
        conn.commit()

    conn.close()
    return redirect(url_for("order_details", order_id=order_id))

# ---------- SELLER DASHBOARD ----------
@app.route('/seller-dashboard', methods=["GET","POST"])
def seller_dashboard():
    if "user" not in session or session.get("user_role") != "seller":
        return redirect(url_for('login', role='seller'))

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
            return redirect(url_for('seller_dashboard'))
        except Exception as e:
            print(f"Seller dashboard error: {e}")

    return render_template("admin.html", categories=categories)

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
        ("Tomato Seeds", 150, "/static/images/tomato_seeds.jpg", 1, "High-quality hybrid tomato seeds, disease resistant"),
        ("Wheat Seeds", 200, "/static/images/wheat_seeds.jpg", 1, "Premium quality wheat seeds for better yield"),
        ("Rice Seeds", 180, "/static/images/rice_seeds.jpg", 1, "Long grain rice seeds, high germination rate"),

        # Fertilizers
        ("NPK Fertilizer 20-20-20", 450, "/static/images/npk_fertilizer.jpg", 2, "Balanced NPK fertilizer for all crops"),
        ("Organic Manure", 300, "/static/images/organic_manure.jpg", 2, "100% organic manure, improves soil health"),
        ("Urea Fertilizer", 250, "/static/images/urea_fertilizer.jpg", 2, "Nitrogen-rich fertilizer for leafy vegetables"),

        # Pesticides
        ("Insecticide Spray", 350, "/static/images/insecticide_spray.jpg", 3, "Effective against common garden pests"),
        ("Fungicide Powder", 280, "/static/images/fungicide_powder.jpg", 3, "Controls fungal diseases in plants"),
        ("Herbicide Solution", 420, "/static/images/herbicide_solution.jpg", 3, "Selective weed control solution"),

        # Tools
        ("Garden Hoe", 180, "/static/images/garden_hoe.jpg", 4, "Sturdy garden hoe for soil cultivation"),
        ("Watering Can", 120, "/static/images/watering_can.jpg", 4, "5-liter capacity watering can"),
        ("Pruning Shears", 250, "/static/images/pruning_shears.jpg", 4, "Professional pruning shears"),

        # Machinery
        ("Hand Tractor", 15000, "/static/images/hand_tractor.jpg", 5, "Mini hand tractor for small farms"),
        ("Sprayer Pump", 850, "/static/images/sprayer_pump.jpg", 5, "Battery operated sprayer pump"),
        ("Seed Drill", 2200, "/static/images/seed_drill.jpg", 5, "Manual seed drill for precise planting")
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


