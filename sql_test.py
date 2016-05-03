import sqlite3
import os

# Switch to app directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

conn = sqlite3.connect('site.db')

c = conn.cursor()


# Create table
print "Dropping table"
try:
    c.execute("DROP TABLE site")
except:
    pass
    
print "Creating table"
c.execute("CREATE TABLE site (id INTEGER PRIMARY KEY, url TEXT, count INTEGER);")


url = ('http://www.news.com')

# Insert a row of data
print "Inserting dummy site"
c.execute("INSERT INTO site VAlUES (0,?, 2)",(url,))

print "Getting data"
t = ('0')
c.execute("SELECT * FROM site WHERE url=?",(url,))
data = c.fetchone()

print "Updating count"
value = list(data)[2]
value += 1
c.execute("UPDATE site SET count=? WHERE url=?",(value,url))

print "Getting data"
t = ('0')
c.execute("SELECT * FROM site WHERE url=?",(url,))
data = c.fetchone()

print data

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()