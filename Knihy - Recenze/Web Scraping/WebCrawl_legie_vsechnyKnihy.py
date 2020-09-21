from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import WebScrape_legie

my_url='https://www.legie.info/kniha/zacina/num'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#vyhledani hledanych dat v html
page_soup = soup(page_html, "html.parser")

content = page_soup.findAll("div",{"id":"content"})

char_pages_html=page_soup.find("div",{"class":"c"}).findAll("a")
char_pages = []
for x in char_pages_html:
	char_pages+=[x["href"]]


for char in char_pages:
	if(char != "kniha/zacina/num"):
		my_url="https://www.legie.info/"+char


		uClient = uReq(my_url)
		page_html = uClient.read()
		uClient.close()

		#vyhledani hledanych dat v html
		page_soup = soup(page_html, "html.parser")
		content = page_soup.find("div",{"id":"content"})  

		books=content.table.findAll("a")    
		x=0
		for book in books:
			if(book["href"][0]=='k'):
				WebScrape_legie.WebScrape("https://www.legie.info/"+book["href"])
				x+=1
				if(x>5):
					exit()