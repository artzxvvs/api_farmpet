import sqlite3
p = r'c:\Users\geti\Downloads\brnhur gostoso\api_farmpet\banco.db'
conn = sqlite3.connect(p)
cur = conn.cursor()
try:
    cur.execute("PRAGMA table_info('transacoes')")
    cols = cur.fetchall()
    print('COLUMNS:', cols)
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='transacoes'")
    print('CREATE:', cur.fetchone())
except Exception as e:
    print('ERR', e)
finally:
    conn.close()
