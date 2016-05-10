from robot import *

# Gets list of websites from text document and sets up objects
sites = []
with open('websites.txt', "r") as f:
    for line in f:
        line = line.strip("\n")
        page = Page(line)
        site = Site(page)
        sites.append(site)

# Loops through each site ibhect for MAX_TRACK number of pages
count = 0
MAX_TRACK = 2

while count < MAX_TRACK:
    start = time.time()
    for site in sites:
        try:
            site.update()
        except:
            pass

    # Delays for two seconds before running through sites again (robot compliance)
    while time.time() < (start + 2):
        pass

    count += 1

#close sites
for site in sites:
    site.conn.close()