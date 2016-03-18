from bs4 import BeautifulSoup
import csv
import urllib2


def add_to_all_links(page_links, all_links):
    """
    Accepts page_links [list]
    Iterates through page_links and checks to see if the link is not already in all_links [list] 
        If not, appends link to all_links
    Does not return anything
    """
    for link in page_links:
        if link not in all_links:
            all_links.append(link)
    print all_links
    return all_links

def scan_for_links(soup):
    """
    Takes soup [Beautiful Soup object]
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
    Uses urllib2 to generate a request and respone
    Creates a soup [Beautiful Soup instance] from the response using html.parser
    Returns soup
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
    	link = expand_link(link, start_page)
        if is_internal(link, start_page):
            internal_links.append(link)
    return internal_links

def find_domain(webpage):
    """
    Accepts webpage [string] and removes the Protocol, Subdomain and Path. Returns domain [string]
    Example: if webpage is "http://news.google.com/world" then domain is "google.com"
    """
    return webpage.split('/')[2]

def is_internal(link, start_page):
    """
    THIS NEEDS FIXING. RETURNS FALSE FOR INTERNAL NEWS PAGES
    Checks webpage [string] against start_page [string]
    Passes both to find_domain [function] which strips them down to the URL domain (ie: www.google.com)
    Checks both domains against each other to find if they match.
    Returns True if they are from the same domain 
    """
    try: 
        link_domain = find_domain(link)
        start_page_domain = find_domain(start_page)
        return link_domain in start_page_domain or start_page_domain in link_domain
        # Uses 'or' to see if either domain fits inside the other.
        # this ensures that google.com and www.google.com match regardless of which way around they are

    except:
        return False # if link not valid

def is_valid(link):
    """
    Accepts link [string]
    Checks if link is empty, or a relative link (# or ?). Returns False
    Checks if link against skip_protocols [list]. Returns False.
    Checks if end of link matches matches skip_extensions [list]. Returns false
    Returns True.
    """
    skip_extensions = ['jpg', 'jpeg', 'png', 'tiff', 'gif', 'apng', 'mng', 'svg', 'pdf', 'bmp', 'ico', 'xbm']
    skip_protocols = ['feed' 'ftp', 'rss']

    if link == '' or link[0] == '#' or link[0] == '?':
        return False 

    for protocol in skip_protocols:
        if link[:len(protocol)] == protocol:
            return False

    for extension in skip_extensions:
        if link[-len(extension):] == extension:
            return False
    
    return True


def expand_link(link, start_page):
    """
    Accepts link [string] and start_page [string] both containing URLs
    If link starts with a '/' (relative link) and adds start page to new_link [string] to create absolute path
        Else if start_page [string] ends in '/',  strips the '/' it to prevent duplicate in path
    Returns new_link
    """
    if link[0] == '/':
        if start_page[-1:] == '/':
            new_link = start_page[:-1] + link # If relative URL ends in a '/' - removes it so you don't get '//' in newlink
        else:
            new_link = start_page + link
    else:
        new_link = link
        
    return new_link

def scan_website(start_page, max_pages):
    """
    Accepts start_page [string], a URL, and max_pages[int]
    Adds start_page to pages_to_track [list]. Then scans page for links and adds
    internal links to pages_to_track.
    Adds links found to all_links [list]
    Returns all_links.
    """
    pages_to_track = [start_page]
    pages_tracked = []
    all_links = []
    print all_links
    count = 0 # visual count of pages tracked (is displayed to console)
    while count < max_pages and len(pages_to_track) > 0:
        try:
            current_page = pages_to_track.pop(0)
            soup = get_soup(current_page)
            page_links = scan_for_links(soup)
            all_links = add_to_all_links(page_links, all_links)
            internal_links = find_internal_links(page_links, start_page)            
            for page in internal_links:
                if page not in pages_tracked and page not in pages_to_track:
                    if is_valid(page):
                        pages_to_track.append(page)
        except:
            pass # skips pages that don't respond

        count += 1
        print "Number of pages tracked: " + str(count)
        
        if current_page not in pages_tracked:
            pages_tracked.append(current_page)

    return all_links

all_links = scan_website('http://news.bbc.co.uk', 20)

# Writes alL_links to CSV file
with open('pages_tracked.csv', 'wb') as f:
    writer = csv.writer(f)
    for row in all_links:
        writer.writerow([row])