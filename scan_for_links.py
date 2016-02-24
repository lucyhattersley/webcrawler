from bs4 import BeautifulSoup
import urllib2

def scan_for_links(soup):
    """
    Takes a soup object (containing a web page response).
    Finds all  links and adds to page_links (a list)
    Returns page_links
    """
    page_links = []

    for link in soup.find_all('a'):
        linkstring = (str(link.get('href'))) #typecast to string
        if linkstring != '' and linkstring[0] == '#': # skips anchors
            pass
        elif linkstring != '' and linkstring [0] == '/': # Checks for relative URLs
            if webpage[-1:] == '/':
                print "webage[-1:] == '/' ran"
                newlink = webpage[:-1] + linkstring # If relative URL ends in a '/' - removes it so you don't get '//' in newlink
            else:
                newlink = webpage + linkstring # places base webpage in front of relative URL to form a full link
        else:
            newlink = linkstring
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

soup = get_soup('http://news.bbc.co.uk')
links = scan_for_links(soup)
print links