# This creates a 'links.txt' file containing all html links found in website

from bs4 import BeautifulSoup
import urllib2


def write_to_file(page_links):
    """
    Accepts page_links (a list)
    Opens the all_links.txt file (in amend mode)
    Iterates through page_links and checks to see if the link is not already in the file (if not, writes the link to the end of the file)
    Does not return anything
    """
    with open('all_links.txt', "a") as all_links:
        for link in page_links:
            if link not in open('all_links.txt').read(): #prevents duplicates 
                all_links.write(link)
                all_links.write('\n') 
        all_links.close()

    return

def scan_for_links(soup):
    """
    Takes a soup object (containing a web page response).
    Finds all  links and adds to page_links (a list)
    Returns page_links
    """
    page_links = []

    # Finds all links in page
    # THIS NEEDS TO SORT OUT HTTP://WWW PROBLEM. SO IS GOING TO BE EVEN CLUMSIER.
    # PERHAPS FIGURE OUT WAY TO TIDY THIS UP WHILST FIXING URL PROBLEM
    # THIS IS CLUNKY CONSIER PUTTING ANCHORS AND RELATIVE URLS INTO SEPARATE FUNCTION
    for link in soup.find_all('a'):
        linkstring = (str(link.get('href'))) #typecast to string
        if linkstring != '' and linkstring[0] == '#': # skips anchors
            pass
        elif linkstring != '' and linkstring [0] == '/': # Checks for relative URLs
            if webpage[-1:] == '/':
                newlink = webpage[:-1] + linkstring # If relative URL ends in a '/' - removes it so you don't get '//' in newlink
            else:
                newlink = webpage + linkstring # places base webpage in front of relative URL to form a full link
        else:
            newlink = linkstring
        if newlink not in page_links:
            page_links.append(newlink)

    return page_links

def get_soup(webpage):
    """
    Accepts webpage (a string) containing a URL
    Uses urllib2 to generate a request, then a respons
    Creates a soup object from the response using html.parser
    Returns soup (a Beautiful Soup object)
    """
    request = urllib2.Request(webpage)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    return soup

def find_internal_links(page_links, webpage, domain):
    """
    Accepts page_links (a list) containing URLs and a single webpage
    Iterates through page links and amends links that match the webpage to internal links (a list)
    Returns internal_links
    """
    internal_links = []

    for link in page_links:
        if find_domain(link) == domain:
            internal_links.append(link)
    return internal_links

def find_domain(webpage):
    """
    Accepts webpage (a string) and removes the Protocol, Subdomain and Path. Returns domain (a string).
    EX: if webpage is "http://news.google.com/world" then domain is "google.com"
    """
    domain = ''

    start = False
    stop = False
    for c in webpage:
        if start == True and c == '/': # Finds the first '/' after the dots and stops adding chars to domain
            stop = True
        if start == True and stop == False:
            domain = domain + c # between stop and start so it doesn't add the '.' and '/' to domain
        if c == '.': # finds the first '.' in the URL and then starts adding chars to domain
            start = True
    return domain

start = 'http://www.ladywelltavern.com'
domain = find_domain(start)

#set up tracking lists
pages_to_track = []
pages_to_track.append(start)
pages_tracked = []

count = 0 # visual count of pages tracked (is displayed to console)

while len(pages_tracked) < 100 and len(pages_to_track) > 0:
    
    try:
        webpage = pages_to_track.pop(0)
        soup = get_soup(webpage)
        page_links = scan_for_links(soup)

        write_to_file(page_links)

        internal_links = find_internal_links(page_links, webpage, domain)

        for page in internal_links:
            if page not in pages_tracked or page not in pages_to_track:
                pages_to_track.append(page)
                with open('pages_to_track.txt', 'a') as f:
                    f.write(page)
                    f.write('\n')

        count += 1
        print "Number of pages tracked: " + str(count)

    except:
        pass # skips pages that don't respond
    pages_tracked.append(webpage)
