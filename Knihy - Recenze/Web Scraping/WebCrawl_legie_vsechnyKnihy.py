from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import WebScrape_legie

#CrawlPart = ID pismena ve kterém se mají hledat URL
#BookPart = id knihy konkrétního písmena od které se mají hledat url
#priklad FindBookUrls(2,100)
#bude hledat url knih začinajici na pismeno A ale bude ignorovat 100 prvnih knih zacinajicich na A
def FindBookUrls(CrawlPart,BookPart=0):

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


	char=char_pages[CrawlPart-1]
	if(char != "kniha/zacina/num"):
		my_url="https://www.legie.info/"+char


		uClient = uReq(my_url)
		page_html = uClient.read()
		uClient.close()

		#vyhledani hledanych dat v html
		page_soup = soup(page_html, "html.parser")
	
	content = page_soup.find("div",{"id":"content"})  
	books=content.table.findAll("a")    

	bookCount=0
	for book in books:
		if(book["href"][0]=='k'):
			bookCount+=1
			if(BookPart<bookCount):
				WebScrape_legie.WebScrape("https://www.legie.info/"+book["href"])

