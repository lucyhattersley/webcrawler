from robot import *

sites = []

with open('websites.txt', "r") as f:
    for line in f:
        line = line.strip("\n")
        page = Page(line)
        site = Site(page)
        sites.append(site)

i = 0
while i < 2:
    for site in sites:
        start = time.time()
        site.update()
        end = time.time()
        while (end - start) < 2:
            end = time.time()
            print end - start
    i += 1

#close site
#site.conn.close()