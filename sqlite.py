import sqlite3

conn = sqlite3.connect('database.db')

print("Opened database successfully")

try:
    conn.execute('DROP TABLE messages')
except:
    pass

conn.execute('CREATE TABLE messages (ID INTEGER PRIMARY KEY AUTOINCREMENT, identifier TEXT, message_body TEXT, date_created INT, fetched INT DEFAULT 0)')
print("Table created successfully")
conn.close()
