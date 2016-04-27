from bs4 import BeautifulSoup
import csv
import requests
import time
import string

class Site(object):
    def __init__(self, url):
        self.url = url

class Page(object):
    def __init__(self,url):
        self.url = url

    def find_domain(self):
        """
        Accepts webpage [string] and removes the Protocol, Subdomain and Path. Returns domain [string]
        Example: if webpage is "http://news.google.com/world" then domain is "google.com"
        """
        domain = self.url.split('/')[2]
        return domain



# create site to track (using 'www.trustedreviews.com' as example)
website = Site('http://www.trustedreviews.com/news')

start_page = Page(website.url)
domain = start_page.find_domain()

print domain