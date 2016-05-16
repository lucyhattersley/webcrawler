from bs4 import BeautifulSoup
import csv
import requests
import time
from reppy.cache import RobotsCache
import sqlite3
import os

class Site(object):
    def __init__(self, homepage):
        self.homepage = homepage # a Page object
        self.pages_to_track = [homepage] # List of Page objects
        self.pages_tracked = [] # List of url strings

        # SETTING UP SQL database
        # Changing directory to dbase (inside app directory)
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname + '/dbase/')

        # Strips out http:// and dots and slash from domain name and adds '.db' to end as database file
        homepage = homepage.get_url()
        dbase = ''.join(homepage.split('.')[1:]) + '.db'
        dbase = dbase.replace('/','')

        # Create connection and c cursor (used to execute commands)
        self.conn = sqlite3.connect(dbase)
        self.c = self.conn.cursor()

        # Clear database if it already exists
        try:
            self.c.execute("DROP TABLE site")
        except:
            pass

        # Create table
        self.c.execute("CREATE TABLE site (url TEXT, count INTEGER);")

    def update(self):
        """
        Pops a page from the pages_to_track [list]
        Finds all the links in that page
        If the link is not in pages_tracked
            Adds new links to the database (with the value 1)
        Else
            Updates link count in database by 1
        Adds link to pages_tracked 
        """
        page = self.pages_to_track.pop()
        while self.robot_pass(page) == False:
            print "Robot blocked: " + page.get_url()
            page = self.pages_to_track.pop()
        print "Now tracking: " + page.get_url()

        internal_links = page.get_internal_links()
        pages_tracked = self.get_pages_tracked()

        while len(internal_links) > 0:
            link = internal_links.pop()
            if page.is_valid(link):
                self.expand_link(link)
                if link not in pages_tracked:
                    self.set_page_tracked(link)
                    self.set_pages_to_track(self.expand_link(link))
                    self.c.execute("INSERT INTO site VAlUES (?, 1)",(link,))
                    self.conn.commit()
                else:
                    self.c.execute("SELECT * FROM site WHERE url=?",(link,))
                    data = self.c.fetchone()
                    value = list(data)[1]
                    value += 1
                    self.c.execute("UPDATE site SET count=? WHERE url=?",(value,link))
                    self.conn.commit()

    def get_homepage(self):
        return self.homepage.get_url()

    def get_pages_to_track(self):
        return self.pages_to_track

    def get_pages_tracked(self):
        return self.pages_tracked

    def get_all_links(self):
        return self.all_links

    def set_page_tracked(self,link):
        self.pages_tracked.append(link)

    def set_pages_to_track(self,link):
        self.pages_to_track.append(Page(link))

    def expand_link(self,link):
        """
        Accepts link [string]
        If link starts with a '/' (relative link) and adds home page to new_link [string] to create absolute path
            Else if start_page [string] ends in '/',  strips the '/' it to prevent duplicate in path
        Returns new_link
        """
        homepage = self.get_homepage()
        if link == "":
            return homepage
        if link[0] == '/':
            if homepage[-1:] == '/':
                new_link = homepage[:-1] + link # If relative URL ends in a '/' - removes it so you don't get '//' in newlink
            else:
                new_link = homepage + link
        else:
            new_link = link
        return new_link

    def robot_pass(self,page):
        """
        Accepts page [object]
        Creates instance of RobotsCache (from reppy)
        Passes URL of page as string into robots.allowed method
        Returns True or False
        """
        robots = RobotsCache()
        return robots.allowed(page.get_url(), '*')

class Page(object):
    def __init__(self,url):
        self.url = url
    
    def get_url(self):
        return self.url

    def get_links(self):
        """
        Accepts soup [Beautiful Soup object]
        Finds all URLs in soup and adds to links [list]
        Returns links
        """
        soup = self.get_soup()
        links = []
        for link in soup.find_all('a'):
            links.append(str(link.get('href')))

        return links

    def get_internal_links(self):
        """
        Uses get_links method to get all links
        Uses get_domain method to find domain page
        If link is_valid and if it matches domain
            adds link to internal_links [list]
        Returns internal_links
        """
        internal_links = []
        for link in self.get_links():
            try:
                if self.is_valid(link) and link.split('/')[2] == self.get_domain() or link[0] == '/':
                    internal_links.append(link)
            except:
                pass
        return internal_links

    def get_domain(self):
        """
        Removes the Protocol, Subdomain and Path and returns as a string
        Example: if webpage is "http://news.google.com/world" then domain is "google.com"
        """
        return self.get_url().split('/')[2]

    def same_domain(self,other):
        """
        Accepts other [Page object]
        Checks to see if self and other belong to the same domain
        Returns True or False
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

    def get_soup(self):
        """
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
        response = requests.get(self.get_url(), headers=request_headers)
        response.status_code
        soup = BeautifulSoup(response.text, "html.parser")
    
        return soup

    def is_valid(self, link):
        """
        Accepts link [string]
        If link is empty, or a relative link (# or ?). Returns False
        If link against skip_protocols [list]. Returns False.
        If end of link matches matches skip_extensions [list]. Returns False
        Else returns True.
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