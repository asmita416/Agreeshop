import sqlite3
from tabulate import tabulate

def view_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    print("🌾 AGRISHOP DATABASE VIEWER 🌾")
    print("=" * 50)

    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    print(f"\n📋 TABLES FOUND: {len(tables)}")
    for table in tables:
        print(f"  • {table[0]}")

    # Show categories
    print(f"\n📂 CATEGORIES:")
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    if categories:
        print(tabulate(categories, headers=['ID', 'Name', 'Description'], tablefmt='grid'))
    else:
        print("  No categories found")

    # Show products by category
    print(f"\n🛍️ PRODUCTS BY CATEGORY:")
    for category in categories:
        cat_id, cat_name, cat_desc = category
        print(f"\n🌱 {cat_name.upper()}:")
        cursor.execute("""
            SELECT p.id, p.name, p.price, p.description
            FROM products p
            WHERE p.category_id = ?
        """, (cat_id,))
        products = cursor.fetchall()

        if products:
            print(tabulate(products, headers=['ID', 'Name', 'Price', 'Description'], tablefmt='grid'))
        else:
            print("  No products in this category")

    # Show users
    print(f"\n👥 REGISTERED USERS:")
    cursor.execute("SELECT id, username FROM users")
    users = cursor.fetchall()
    if users:
        print(tabulate(users, headers=['ID', 'Username'], tablefmt='grid'))
    else:
        print("  No users registered yet")

    conn.close()

if __name__ == "__main__":
    view_database()