from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    

my_url='https://www.cbdb.cz/kniha-10-harry-potter-a-fenixuv-rad-harry-potter-and-the-order-of-the-phoenix?order_comments=time'

#otevre url a precte html zadaneho url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#vyhledani hledanych dat v html
page_soup = soup(page_html, "html.parser")
genres = page_soup.findAll("span",{"itemprop":"genre"})
author = page_soup.find("a",{"itemprop":"author"}).text
annotation = page_soup.find("div",{"id":"book_annotation"})
annotation.b.decompose()
reviews = page_soup.findAll("div",{"class":"comment"})


#tisk vyhledanych dat
print("Nazev: ",page_soup.h1.text)
for genre in genres:
	print("Zanr: ",genre.text)
print("Autor: ",author)
print("Anotace: ",annotation.text)

for review in reviews:
	username=review.div.img["alt"]
	userid=review.div.img["src"]
	userid=userid[6:-4]

	header=review.find("div",{"class":"comment_header"})
	rating=header.img["alt"] 
	date=header.find("span",{"class":"date_span"}).text
	comment=review.find("div",{"class":"comment_content"}).text
	comment=comment.replace('\n',' ')
	print(username+'\t'+userid+'\t'+date+'\t'+rating+'\t'+comment+'\n') 