import sqlite3, os

# Backend database
backend_db = r'C:\Users\LENOVO\Documents\salatify\backend\database.db'
print("=== BACKEND DATABASE ===")
print(f"Path: {backend_db}")
print(f"Exists: {os.path.exists(backend_db)}")

if os.path.exists(backend_db):
    conn = sqlite3.connect(backend_db)
    c = conn.cursor()
    # Check all tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print(f"Tables: {[t[0] for t in tables]}")
    
    for table_name in ['surah', 'kategori_doa', 'doa']:
        try:
            c.execute(f'SELECT count(*) FROM {table_name}')
            count = c.fetchone()[0]
            print(f"  {table_name}: {count}")
        except Exception as e:
            print(f"  {table_name}: ERROR - {e}")
    
    # Show sample data from each table
    for table_name in ['surah', 'kategori_doa', 'doa']:
        try:
            c.execute(f'SELECT * FROM {table_name} LIMIT 3')
            rows = c.fetchall()
            print(f"  {table_name} sample: {rows}")
        except Exception as e:
            print(f"  {table_name} sample: ERROR - {e}")
    
    conn.close()
else:
    print("  File not found")

# Kivy database
print("\n=== KIVY DATABASE ===")
kivy_db_dir = os.path.join(os.path.expanduser("~"), ".salatify")
kivy_db = os.path.join(kivy_db_dir, "salatify.db")
print(f"Path: {kivy_db}")
print(f"Exists: {os.path.exists(kivy_db)}")

if os.path.exists(kivy_db):
    conn = sqlite3.connect(kivy_db)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print(f"Tables: {[t[0] for t in tables]}")
    
    for table_name in ['surah', 'kategori_doa', 'doa']:
        try:
            c.execute(f'SELECT count(*) FROM {table_name}')
            count = c.fetchone()[0]
            print(f"  {table_name}: {count}")
        except Exception as e:
            print(f"  {table_name}: ERROR - {e}")
    
    for table_name in ['surah', 'kategori_doa', 'doa']:
        try:
            c.execute(f'SELECT * FROM {table_name} LIMIT 3')
            rows = c.fetchall()
            print(f"  {table_name} sample: {rows}")
        except Exception as e:
            print(f"  {table_name} sample: ERROR - {e}")
    
    conn.close()
else:
    print("  File not found")