from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup  


my_url='https://www.databazeknih.cz/knihy/harry-potter-harry-potter-a-fenixuv-rad-13'

#otevre url a precte html zadaneho url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#vyhledani hledanych dat v html
page_soup = soup(page_html, "html.parser")

Nazev = page_soup.find("h1",{"itemprop":"name"}).text
print(Nazev)