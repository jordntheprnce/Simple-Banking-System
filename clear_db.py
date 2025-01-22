import sqlite3

# connecting to new database
conn = sqlite3.connect('card.s3db')

# creating cursor
c = conn.cursor()
c.execute('DROP TABLE card')
c.execute('SELECT name FROM sqlite_master WHERE type="table"')
print(c.fetchone())