import sqlite3, os
dbpath = r'C:\Users\LENOVO\Documents\salatify\backend\database.db'
conn = sqlite3.connect(dbpath)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('Tables:', c.fetchall())
if 'surah' in [t[0] for t in c.fetchall()]:
    c.execute('SELECT count(*) FROM surah')
    print('surah count:', c.fetchone()[0])
    c.execute('SELECT * FROM surah LIMIT 3')
    print('surah sample:', c.fetchall())
if 'kategori_doa' in [t[0] for t in c.fetchall()]:
    c.execute('SELECT count(*) FROM kategori_doa')
    print('kategori_doa count:', c.fetchone()[0])
if 'doa' in [t[0] for t in c.fetchall()]:
    c.execute('SELECT count(*) FROM doa')
    print('doa count:', c.fetchone()[0])
conn.close()