from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    

my_url='https://www.databazeknih.cz/zanry/architektura-31?dle=az&id=1'

#otevre url a precte html zadaneho url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#vyhledani hledanych dat v html
page_soup = soup(page_html, "html.parser")

content = page_soup.find("div",{"id":"content"})  

leftside=content.find("div",{"id":"left_less"}) 
rightside=content.find("div",{"id":"right_more"})  

zanry=rightside.div.ul.findAll("li")

for zanr in zanry:
	if(zanr.a is not None):
		zanr_url=zanr.a["href"]
	else:
		zanr_url="https://www.databazeknih.cz/zanry/architektura-31?dle=az"

	page_count=int(leftside.find("div",{"class":"pager"}).findAll("a")[-1].text)
	print("PageCount= ",page_count)
	page_count=1

	for page in range(1,page_count+1):
		my_url=zanr_url+"&id="+str(page)
		#otevre url a precte html zadaneho url
		uClient = uReq(my_url)
		page_html = uClient.read()
		uClient.close()

		#vyhledani hledanych dat v html
		page_soup = soup(page_html, "html.parser")

		content = page_soup.find("div",{"id":"content"})  

		leftside=content.find("div",{"id":"left_less"}) 
		
		knihy=leftside.findAll("a",{"class":"biggest odr"})#vsechny knihy na aktualni strance
		for kniha in knihy:
			print(kniha["href"])
