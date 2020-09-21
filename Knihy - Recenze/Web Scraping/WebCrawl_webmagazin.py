from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import WebScrape_cbdb

my_url='https://www.cbdb.cz/knihy-0'

#otevre url a precte html zadaneho url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#vyhledani hledanych dat v html
page_soup = soup(page_html, "html.parser")
