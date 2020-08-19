from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import WebScrape_cbdb
#pocet vsech stranek = 2216
def FindBookUrls(idLow,idHigh):
	my_url='https://www.cbdb.cz/knihy-0'

	#otevre url a precte html zadaneho url
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	#vyhledani hledanych dat v html
	page_soup = soup(page_html, "html.parser")

	content = page_soup.find("div",{"id":"content"})  
	char_pages_html = content.findAll("a",{"class":"textlist_item_select round_mini"})  
	char_pages = []
	for char in char_pages_html:
		char_pages+=[char["href"]]

	char_pages.insert(0,"knihy-0")

	PageId=1
	for char in char_pages:
		if(char != "knihy-0"):
			my_url="https://www.cbdb.cz/"+char

			uClient = uReq(my_url)
			page_html = uClient.read()
			uClient.close()

			#vyhledani hledanych dat v html
			page_soup = soup(page_html, "html.parser")
			content = page_soup.find("div",{"id":"content"})  
			
		try:
			page_count=int(content.findAll("a",{"class":"topic_paging_item round_mini"})[-1].text)
		except IndexError:
			page_count=1


		if(PageId+page_count<idLow):
			PageId+=page_count
			continue
		for page in range(1,page_count+1):
			if(page!=1):
				my_url="https://www.cbdb.cz/"+char+'-'+str(page)

				uClient = uReq(my_url)
				page_html = uClient.read()
				uClient.close()

				#vyhledani hledanych dat v html
				page_soup = soup(page_html, "html.parser")
				content = page_soup.find("div",{"id":"content"})  


			books=content.table.findAll("a")    
			for book in books:
				if(book["href"][0]=='k'):
					if(idHigh >= PageId >= idLow ):
						WebScrape_cbdb.WebScrape_reviews("https://www.cbdb.cz/"+book["href"])
						
					elif(PageId > idHigh):
						exit()
			PageId+=1