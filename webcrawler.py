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
    NOTE! THIS CODE IS STILL SCRAPPY. CONSIDER FIXING RELATIVE URLS IN A SEPARATE AREA / FUNCTION
    Takes soup (a Beautiful Soup object containing a web page response) and current_page (a string).
    current_page is required to add in front of relative URLs 
    Finds all  links and adds to page_links (a list)
    Returns page_links
    """
    page_links = []

    for soup_link in soup.find_all('a'):
        link = (str(soup_link.get('href'))) #typecast soup_link to string
        if link == '' or link[0] == '#': # skips blanks and anchors
            pass
        elif link[0] == '/': # Checks for relative URLs
            if link[-1:] == '/':
                newlink = start_page[:-1] + link # If relative URL ends in a '/' - removes it so you don't get '//' in newlink
            else:
                newlink = start_page + link # places base webpage in front of relative URL to form a full link
        else:
            newlink = link
        if newlink not in page_links:
            page_links.append(newlink)
    print "Page links: " + str(page_links)
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
        if is_internal(webpage, domain):
            internal_links.append(link)
    return internal_links

def find_domain(webpage):
    """
    Accepts webpage (a string) and removes the Protocol, Subdomain and Path. Returns domain (a string).
    EX: if webpage is "http://news.google.com/world" then domain is "google.com"
    """
    return webpage.split('/')[2]

def is_internal(webpage, start_page):
    """
    Checks webpage (a string representing a URL) against the startpage (a string, representing a URL)
    Strips both down to find the domain
    Returns true if they are from the same domain 
    """
    webpage_dom = find_domain(webpage)
    print "webpage_dom is: " + webpage_dom
    startpage_dom = find_domain(start_page)
    print "startpage_dom is: " + start_page_dom

    return webpage_dom in start_page_dom or start_page_dom in webpage_dom

start_page = 'http://www.ladywelltavern.com'

#set up tracking lists
pages_to_track = [start_page]
pages_tracked = []

count = 0 # visual count of pages tracked (is displayed to console)

while len(pages_tracked) < 100 and len(pages_to_track) > 0:
    
    try:
        current_page = pages_to_track.pop(0)
        soup = get_soup(current_page)

        page_links = scan_for_links(soup, current_page)
        write_to_file(page_links)
        internal_links = find_internal_links(page_links, current_page, start_page)

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
    
    pages_tracked.append(current_page)