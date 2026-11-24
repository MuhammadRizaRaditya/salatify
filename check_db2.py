import sqlite3
conn = sqlite3.connect(r'C:\Users\LENOVO\Documents\salatify\backend\database.db')
c = conn.cursor()
c.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL")
rows = c.fetchall()
print('Schema statements:')
for r in rows:
    print(r[0])
conn.close()