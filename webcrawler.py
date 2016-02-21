# This creates a 'links.txt' file containing all html links found in website

from bs4 import BeautifulSoup
import urllib2

def scan_for_links(soup, webpage):
    """
    Takes a soup object (containing a web page response) and webpage, a string of the site's URL.
    Finds all  links and adds new links to all_links.txt file
    Returns add_to_tracklist, a list of internal links from the site (strings) to be added to pages_to_track
    """
    current_page_links = []
    add_to_tracklist = []

    # Finds all links in page and appends to current_page_links list
    for link in soup.find_all('a'):
        linkstring = (str(link.get('href'))) #typecast to string
        if linkstring != '' and linkstring[0] == '#': #removes anchors
            pass
        elif linkstring != '' and linkstring [0] == '/': # Makes sure link contains main URL
            newlink = webpage + linkstring
        else:
            newlink = linkstring
        
        if newlink not in current_page_links:
            current_page_links.append(newlink) 

    # NOTE: SPLIT THIS OUT INTO SEP FUNCTION
    # Write all links to file
    all_links = open('all_links.txt', "a")
    for link in current_page_links:
        if link not in open('all_links.txt').read(): #prevents duplicates 
            all_links.write(link)
            all_links.write('\n')
    # Close links file 
    all_links.close()

    # Creates list of internal URLs
    for link in current_page_links:
        if link[:len(webpage)] == webpage:
            add_to_tracklist.append(link) 

    return add_to_tracklist

# Start page (this will be added to command line eventually)
start = 'http://news.bbc.co.uk'

#set up tracking lists
pages_to_track = []
pages_to_track.append(start)
pages_tracked = []

# This needs tidying up and better comments. Maybe split something out into function
webpage = start
count = 0 # visual count

while len(pages_tracked) < 10 or len(pages_to_track) == 0:

    request = urllib2.Request(webpage)

    # Gets content from web page and passes it into a soup object
    try:
        response = urllib2.urlopen(request)
    except:
        pass # skips pages that don't respond
    soup = BeautifulSoup(response, "html.parser")

    new_pages_found = scan_for_links(soup, webpage)
 
    for page in new_pages_found:
        if page not in pages_to_track:
            pages_to_track.append(page)
    
    if page not in pages_tracked:
        pages_tracked.append(webpage) # keeps track of pages
 
    try:
        webpage = pages_to_track.pop(0)
    except:
        print "No pages left to track"
        break
    
    count += 1
    print "Number of pages tracked: " + str(count)