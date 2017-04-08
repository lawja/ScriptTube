from bs4 import BeautifulSoup
import urllib.request


page = urllib.request.urlopen('https://www.youtube.com').read()

soup = BeautifulSoup(page, 'xml')
