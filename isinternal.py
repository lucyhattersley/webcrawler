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
    return webpage.split('/')[2]

def is_internal(webpage, startpage):
    """
    Checks webpage (a string representing a URL) against the startpage (a string, representing a URL)
    Strips both down to find the domain
    Returns true if they are from the same domain 
    """
    webpage_dom = find_domain(webpage)
    print "webpage_dom is: " + webpage_dom
    startpage_dom = find_domain(startpage)
    print "startpage_dom is: " + startpage_dom

    return webpage_dom in startpage_dom or startpage_dom in webpage_dom

startpage = 'http://www.bbc.co.uk'

pages = ['http://www.bbc.co.uk', 'http://bbc.co.uk', 'http://www.bbc.co.uk/iplayer', 'http://www.telegraph.co.uk']
for page in pages:
    print page
    print is_internal(page, startpage)