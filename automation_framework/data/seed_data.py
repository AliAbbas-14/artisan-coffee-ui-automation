import os
import openpyxl
import sqlite3
from redis_reader import RedisReader

def generate_test_data_excel(filepath: str):
    wb = openpyxl.Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet)

    # 1. MenuProducts Sheet
    ws_menu = wb.create_sheet(title="MenuProducts")
    ws_menu.append(["scenario_id", "product_name", "price", "origin", "flavor_notes"])
    ws_menu.append(["TC_PRD_01", "Black Label Espresso", "$4.50", "COLOMBIA · HUILA · WASHED", "Dark Chocolate, Molasses, Walnut"])
    ws_menu.append(["TC_PRD_02", "Velvet Oat Latte", "$5.50", "ETHIOPIA · YIRGACHEFFE · NATURAL", "Blueberry, Jasmine, Brown Sugar"])
    ws_menu.append(["TC_PRD_03", "Midnight Cold Brew", "$6.00", "GUATEMALA · ANTIGUA · HONEY", "Caramel, Dark Cherry, Smoke"])
    ws_menu.append(["TC_PRD_04", "Pour Over Reserve", "$5.00", "KENYA · KIRINYAGA", "Blackcurrant, Bergamot, Honey"])

    # 2. NewsletterData Sheet
    ws_news = wb.create_sheet(title="NewsletterData")
    ws_news.append(["scenario_id", "email", "expected_status", "description"])
    ws_news.append(["TC_NEWS_01", "ali.abbas.tester@gmail.com", "valid", "Standard corporate email"])
    ws_news.append(["TC_NEWS_02", "coffee.lover2026@outlook.com", "valid", "Customer outlook email"])
    ws_news.append(["TC_NEWS_03", "qa_lead_automation@fast.edu.pk", "valid", "Academic student domain"])
    ws_news.append(["TC_NEWS_04", "invalid-format-email", "invalid", "Malformed email syntax"])

    # 3. BlendData Sheet
    ws_blend = wb.create_sheet(title="BlendData")
    ws_blend.append(["scenario_id", "blend_name", "roast_profile", "intensity"])
    ws_blend.append(["TC_BLD_01", "ESPRESSO NOIR", "Dark French Roast", "High (5/5)"])
    ws_blend.append(["TC_BLD_02", "MORNING GOLD", "Medium City Roast", "Medium (3/5)"])
    ws_blend.append(["TC_BLD_03", "VELVET HOUR", "Light Cinnamon Roast", "Low (2/5)"])

    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    wb.save(filepath)
    print(f"Generated test Excel file: {filepath}")

def seed_sqlite_test_records(db_path: str):
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS CoffeeMenu (
            id TEXT PRIMARY KEY,
            name TEXT UNIQUE,
            price TEXT,
            origin TEXT,
            category TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS NewsletterSubscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    coffees = [
        ('c1', 'Black Label Espresso', '$4.50', 'COLOMBIA · HUILA · WASHED', 'Espresso'),
        ('c2', 'Velvet Oat Latte', '$5.50', 'ETHIOPIA · YIRGACHEFFE · NATURAL', 'Latte'),
        ('c3', 'Midnight Cold Brew', '$6.00', 'GUATEMALA · ANTIGUA · HONEY', 'Cold Brew'),
        ('c4', 'Pour Over Reserve', '$5.00', 'KENYA · KIRINYAGA', 'Filter'),
    ]
    cur.executemany("INSERT OR IGNORE INTO CoffeeMenu (id, name, price, origin, category) VALUES (?, ?, ?, ?, ?)", coffees)
    
    subscribers = [
        ('ali.abbas.tester@gmail.com',),
        ('coffee.lover2026@outlook.com',),
    ]
    cur.executemany("INSERT OR IGNORE INTO NewsletterSubscribers (email) VALUES (?)", subscribers)
    
    conn.commit()
    conn.close()
    print(f"Seeded SQLite DB test records: {db_path}")

def seed_redis_cache():
    reader = RedisReader()
    menu_cache = [
        {"name": "Black Label Espresso", "price": "$4.50"},
        {"name": "Velvet Oat Latte", "price": "$5.50"},
        {"name": "Midnight Cold Brew", "price": "$6.00"}
    ]
    blend_cache = [
        {"blend": "ESPRESSO NOIR", "type": "Dark"},
        {"blend": "MORNING GOLD", "type": "Medium"},
        {"blend": "VELVET HOUR", "type": "Light"}
    ]
    reader.set("cache:menu:signature", menu_cache)
    reader.set("cache:blends:popular", blend_cache)
    print("Seeded Redis cache records (with in-memory fallback)")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.join(current_dir, "test_data.xlsx")
    generate_test_data_excel(excel_path)
    
    root_db = os.path.join(current_dir, "..", "..", "dev.db")
    seed_sqlite_test_records(root_db)
    
    seed_redis_cache()
