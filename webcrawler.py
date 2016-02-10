# This creates a 'links.txt' file containing all html links in a webpage
# NEXT STEPS: Go through links and find valid links.
# Open a child link as a second soup


# References:
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#kinds-of-objects
# http://stackoverflow.com/questions/1843422/get-webpage-contents-with-python
from bs4 import BeautifulSoup
import urllib2

# creates output file in same directory
f = open('links.txt', "w+")

# target webpage
request = urllib2.Request('http://news.bbc.co.uk')
links = []

# Gets content from web page and passes it into a soup object
response = urllib2.urlopen(request)
soup = BeautifulSoup(response)

# Finds all links in page and appends to links list
for link in soup.find_all('a'):
    links.append(link.get('href'))
#    print(link.get('href')) # used to test links

# Writes each link to file
for link in links:
	f.write(link)
	f.write('\n')
f.close()