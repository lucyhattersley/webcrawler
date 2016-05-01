import sqlite3
import os


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
try:
    c.execute("DROP TABLE stocks")
except:
    pass
    
c.execute('''CREATE TABLE stocks
            (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VAlUES ('2006-01-05', 'BUY', 'RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()