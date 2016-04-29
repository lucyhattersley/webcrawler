from bs4 import BeautifulSoup
import csv
import requests
import time
import string

class Site(object):
    def __init__(self, homepage):
        self.homepage = homepage # a Page object
        self.pages_to_track = [homepage] # List of objects
        self.pages_tracked = [] # List of url strings
        self.all_links = [] # List of tuples (url,number of times linked to)
        self.updatecount = 0
  
    def get_homepage(self):
        return self.homepage

    def update_all_links(page_links):
        print "add to all links ran"
        return

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
                soup = current_page.get_soup()
                page_links = current_page.scan_for_links()
                self.add_to_all_links(page_links)
                
                #PICKUP HERE 2016_04_29
                # This code is replacing find_internal_links with same_domain
                # Needs checking
                for link in page_links:
                    page = Page(link)
                    if page.same_domain(self.homepage):
                        internal_links.append(page)
                #ADD INTERNAL LINKs THAT AREN'T IN PAGES TRACKED TO PAGES_TO_TRACK

                print internal_links

            except:
                pass # skips pages that don't respond

            if current_page.get_url() not in self.pages_tracked:
                self.pages_tracked.append(current_page.get_url())
        else:
            pass

        self.updatecount += 1
        print "Updated " + str(self.updatecount) + " time(s)."

        return


    def add_to_all_links(self, page_links):
        """
        Accepts page_links [list] and all_links [list]
        Iterates through page_links and checks to see if the link is not already in all_links [list]. If it finds the link, increases the count by one.
        If not, appends link to all_links
        Returns all_links
        """
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
            link = self.expand_link(link, self.get_url())
            if self.same_domain(link):
                internal_links.append(link)
        return internal_links


class Page(object):
    def __init__(self,url):
        self.url = url
    
    def get_url(self):
        return self.url

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

    def same_domain(self,other):
        """
        Checks to see if two pages [Page object] are from the same domain
        Passes both to find_domain [function] which strips them down to the URL domain (ie: www.google.com)
        Checks both domains against each other to find if they match.
        Returns True if they are from the same domain 
        """
        page1 = self.get_url()
        page2 = other.get_url()

        page1 = page1.split('.',1)[1] #split off protocal and subdomain
        page2 = page2.split('.',1)[1] #split off protocal and subdomain

        print page1
        print page2

        try:
            return page1 in page2 or page2 in page1
            # Uses 'or' to see if either domain fits inside the other.
            # this ensures that google.com and www.google.com match regardless of order

        except:
            return False # if link not valid

    def find_domain(self):
        """
        Accepts webpage [string] and removes the Protocol, Subdomain and Path. Returns domain [string]
        Example: if webpage is "http://news.google.com/world" then domain is "google.com"
        """
        return self.get_url().split('/')[2]

    def get_soup(self):
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
        url = self.get_url()
        response = requests.get(url, headers=request_headers)
        response.status_code
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def scan_for_links(self):
        """
        Takes soup [Beautiful Soup object]
        Finds all URLs in soup and adds to links [list]
        Returns links
        """
        soup = self.get_soup()
        links = []
        for link in soup.find_all('a'):
            links.append(str(link.get('href')))

        return links


# Create site to track (us ing 'www.trustedreviews.com' as example)
# This will be updated with websites.txt integration after a single site is working
page = Page('https://en.wikipedia.org/wiki/Main_Page')
page1 = Page('http://en.wikipedia.org')

site = Site(page)

site.update()
site.update()



# domain = find_domain(startpage)

# # This is going be replaced with SQL
# savefile = 'output2/' + domain + '.csv'

# max_pages = 10000

# print "Starting: " + domain
# all_links = website.scan_website(max_pages)

