from bs4 import BeautifulSoup
import csv
import requests
import time
import string

class Site(object):
    def __init__(self, homepage):
        self.homepage = homepage
        print type(homepage)
        self.pages_to_track = [homepage]
        self.pages_tracked = []
        self.all_pages = []
  
    def get_homepage(self):
        return self.homepage

    # This needs changing from ongoing scan
    # to single update
    # pops a single page from pages_to_track
    # finds all links in page
    # updates pages_to_track, all_links and pages_tracked
    def update(self):
        """
        Accepts self [object]
        Adds start_page to pages_to_track [list]. Then scans page for links and adds
        internal links to pages_to_track.
        Adds links found to all_links [list]
        Returns all_links.
        """
        if len(self.pages_to_track) > 0:
            try:
                current_page = self.pages_to_track.pop(0)
                soup = self.get_soup(current_page)
                page_links = self.scan_for_links(soup)
                print "page_links", page_links
                self.add_to_all_links(page_links)
                print self.all_links
                internal_links = find_internal_links(page_links)
                for page in internal_links:
                    if page not in self.pages_tracked and page not in self.pages_to_track:
                        if is_valid(page):
                            self.pages_to_track.append(page)
            except:
                pass # skips pages that don't respond

            # count += 1
            # print "Number of pages tracked: " + str(count)
            
            # if current_page.get_url() not in self.pages_tracked:
            #     self.pages_tracked.append(current_page.get_url())
        else:
            pass
        return self.all_links

    def add_to_all_links(page_links):
        """
        Accepts page_links [list] and all_links [list]
        Iterates through page_links and checks to see if the link is not already in all_links [list]. If it finds the link, increases the count by one.
        If not, appends link to all_links
        Returns all_links
        """
        print "add_to_all_links ran"
        for link in page_links:
            link_found = False
            for sublist in self.all_links:
                if link == sublist[0]:                
                    link_found = True #prevents duplicate pages                
                    sublist[1] += 1
                    break 
            if link_found == False:
                self.all_links.append([link,1])
        return

    def get_soup(self,url):
        """
        Accepts url [string] containing a URL
        Uses urllib2 to generate a request and respone
        Creates a soup [Beautiful Soup instance] from the response using html.parser
        Returns soup
        """
        request_headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "http://thewebsite.com",
        "Connection": "keep-alive" 
        }
        response = requests.get(url, headers=request_headers)
        response.status_code
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def scan_for_links(self,soup):
        """
        Takes soup [Beautiful Soup object]
        Finds all URLs in soup and adds to links [list]
        Returns links
        """
        #soup = self.get_soup()
        links = []
        for link in soup.find_all('a'):
            links.append(str(link.get('href')))

        return links

class Page(Site):
    def __init__(self,url):
        super(Page, self).__init__()
        self.url = url
    
    def get_url(self):
        return self.url

    def find_internal_links(self):
        """
        Accepts page_links [list] containing URLs and start_page [string] containing the root of the search
        Iterates through page links passed each link to is_internal [function]. This returns True if link domain matches start_page
        Amends links that return True to internal_links [list]
        Returns internal_links
        """
        page_links = self.scan_for_links()
        internal_links = []
        for link in page_links:
            link = expand_link(link, start_page)
            if is_internal(link, start_page):
                internal_links.append(link)
        return internal_links

    def expand_link(self,link, start_page):
        """
        Accepts link [string] and start_page [string] both containing URLs
        If link starts with a '/' (relative link) and adds start page to new_link [string] to create absolute path
            Else if start_page [string] ends in '/',  strips the '/' it to prevent duplicate in path
        Returns new_link
        """
        if link == "":
            return start_page
        if link[0] == '/':
            if start_page[-1:] == '/':
                new_link = start_page[:-1] + link # If relative URL ends in a '/' - removes it so you don't get '//' in newlink
            else:
                new_link = start_page + link
        else:
            new_link = link
        return new_link


    def is_internal(self,url):
        """
        THIS NEEDS FIXING. RETURNS FALSE FOR INTERNAL NEWS PAGES
        Checks webpage [string] against start_page [string]
        Passes both to find_domain [function] which strips them down to the URL domain (ie: www.google.com)
        Checks both domains against each other to find if they match.
        Returns True if they are from the same domain 
        """
        homepage = self.get_homepage()
        try:
            link_domain = self.find_domain(url)
            return link_domain in homepage or homepage in link_domain
            # Uses 'or' to see if either domain fits inside the other.
            # this ensures that google.com and www.google.com match regardless of which way around they are

        except:
            return False # if link not valid


    def find_domain(self,url):
        """
        Accepts webpage [string] and removes the Protocol, Subdomain and Path. Returns domain [string]
        Example: if webpage is "http://news.google.com/world" then domain is "google.com"
        """
        domain = url.split('/')[2]
        return domain


# Create site to track (us ing 'www.trustedreviews.com' as example)
# This will be updated with websites.txt integration after a single site is working
page = Page('http://www.trustedreviews.com')
site = Site(page)




# domain = find_domain(startpage)

# # This is going be replaced with SQL
# savefile = 'output2/' + domain + '.csv'

# max_pages = 10000

# print "Starting: " + domain
# all_links = website.scan_website(max_pages)

