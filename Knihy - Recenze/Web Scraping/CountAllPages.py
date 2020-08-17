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
PageId = 1
AllBookPagesCount=0
for zanr in zanry:
	if(zanr.a is not None):
		zanr_url=zanr.a["href"]
	else:
		zanr_url="https://www.databazeknih.cz/zanry/architektura-31?dle=az"

	page_count=int(leftside.find("div",{"class":"pager"}).findAll("a")[-1].text)
	
	AllBookPagesCount+=page_count

print("databazeknih count:",AllBookPagesCount)


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
AllBookPagesCount=0
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

	AllBookPagesCount+=page_count
print('cbdbCount:',AllBookPagesCount)