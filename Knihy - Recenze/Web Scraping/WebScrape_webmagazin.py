from urllib.request import urlopen as uReq
import urllib
from bs4 import BeautifulSoup as soup    
import os, sys, time

my_url='http://webmagazin.cz/index.php?stype=all&id=10120'
my_url=my_url.encode('utf-8').decode('ascii', 'ignore')

uClient = uReq(my_url)

page_html = uClient.read()
uClient.close()

#vyhledani hledanych dat v html
page_soup = soup(page_html, "html.parser")

obsah = page_soup.find("div",{"class":"clanekObsah"})
datum = page_soup.find("span",{"class":"clDatum"})
autor = page_soup.find("span",{"class":"clAutor"})

print(datum.text.strip())#datum
print(autor.text.strip())#autor
print(obsah.text.replace('\n',' ').replace(chr(13),'').replace('  ','').strip())