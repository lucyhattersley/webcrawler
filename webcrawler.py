# This creates a 'links.txt' file containing all html links found in website

from bs4 import BeautifulSoup
import urllib2


def write_to_file(page_links):
    """
    Accepts page_links [list]
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
    Takes soup [Beautiful Soup object].
    Finds all URLs in soup and adds to links [list]
    Returns links
    """
    links = []
    for link in soup.find_all('a'):
        links.append(str(link.get('href')))

    return links

def get_soup(webpage):
    """
    Accepts webpage [string] containing a URL
    Uses urllib2 to generate a request and respone.
    Creates a soup object from the response using html.parser
    Returns soup (a Beautiful Soup object)
    """
    request = urllib2.Request(webpage)
    response = urllib2.urlopen(request)
    soup = BeautifulSoup(response, "html.parser")
    return soup

def find_internal_links(page_links, start_page):
    """
    Accepts page_links [list] containing URLs and start_page [string] containing the root of the search
    Iterates through page links passed each link to is_internal [function]. This returns True if link domain matches start_page
    Amends links that return True to internal_links [list]
    Returns internal_links
    """
    internal_links = []
    for link in page_links:
        if is_internal(link, start_page):
            internal_links.append(link)
    return internal_links

def find_domain(webpage):
    """
    Accepts webpage [string] and removes the Protocol, Subdomain and Path. Returns domain [string].
    Example: if webpage is "http://news.google.com/world" then domain is "google.com"
    """
    return webpage.split('/')[2]

def is_internal(link, start_page):
    """
    Checks webpage [string] against start_page [string]
    Passes both to find_domain [function] which strips them down to the URL domain (ie: www.google.com)
    Checks both domains against each other to find if they match.
    Returns True if they are from the same domain 
    """
    try: 
        link_domain = find_domain(link)
        start_page_domain = find_domain(start_page)
        # check uses 'or' to see if either domain fits inside the other.
        # this ensures that google.com and www.google.com match regardless of which way around they are
        return link_domain in start_page_domain or start_page_domain in link_domain
    except:
        return False # if link not valid

def is_valid(link):
    """
    NOTE: THIS CHECKS VALID LINKS BUT BASE URLS (IE: WWW.BBC.CO.UK) WILL FAIL. FIGURE OUT FIX
    PERHAPS ENSURE ALL BASE LINKS HAVE '/' AT END?
    Accepts link [string]
    Checks if end of link matches items in valid_extensions [list]
    Returns True if link matches valid_extensions or False if not.
    """
    valid_extensions = ['asp', 'htm', 'html', 'js', 'jsp', 'php', 'xhtml', '/']
    skip_protocols = ['feed' 'ftp', 'rss']

    if link == '' or link[0] == '#' or link[0] == '?':
        return False 

    for protocol in skip_protocols:
        if link[:len(protocol)] == protocol:
            return False

    for extension in valid_extensions:
        if link[-len(extension):] == extension:
            return True
    return False


def expand_link(link, start_page):
    """
    This function needs to expand relative links to full domain links so they can be added to the to_track list (and work)
    Relative links start with a '/' 
    Strips "/" from end of start_page
    Adds start_page and link together
    Returns valid link
    """
    pass
 
start_page = 'http://www.ladywelltavern.com'

#set up tracking lists
pages_to_track = [start_page]
pages_tracked = []

count = 0 # visual count of pages tracked (is displayed to console)

while count < 10 and len(pages_to_track) > 0:
    
    try:
        current_page = pages_to_track.pop(0)
        soup = get_soup(current_page)
        page_links = scan_for_links(soup)
        write_to_file(page_links)
        internal_links = find_internal_links(page_links, start_page)
        for page in internal_links:
            if page not in pages_tracked and page not in pages_to_track:
                if is_valid(page):
                    pages_to_track.append(page)
                    with open('pages_to_track.txt', 'a') as f:
                        f.write(page)
                        f.write('\n')
            f.close()
    except:
        pass # skips pages that don't respond

    count += 1
    print "Number of pages tracked: " + str(count)
    
    if page not in pages_tracked:
        pages_tracked.append(current_page)

with open('pages_tracked.txt', 'a') as f:
    for page in pages_tracked:
        f.write(page)
        f.write('\n')
    f.close()
