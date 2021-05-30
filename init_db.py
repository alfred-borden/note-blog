import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, content_type) VALUES (?, ?, ?)",
            ('First Post', 'Content for the first post', 'excerpt')
            )

cur.execute("INSERT INTO posts (title, content, content_type) VALUES (?, ?, ?)",
            ('Second Post', 'Content for the second post', 'excerpt')
            )

connection.commit()
connection.close()