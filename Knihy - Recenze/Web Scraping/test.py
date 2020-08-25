from urllib.request import urlopen as uReq
import urllib
from bs4 import BeautifulSoup as soup    
import os, sys, time

def Webscrape_head(page_soup):
	Nazev = page_soup.h1.text
	NazevDir = Nazev.translate({ord(i): None for i in '"\/:|<>*?'})

	author = page_soup.find("a",{"itemprop":"author"}).text
	genres = page_soup.findAll("span",{"itemprop":"genre"})
	annotation = page_soup.find("div",{"id":"book_annotation"})
	if(annotation is not None):
		if(annotation.b is not None):
			annotation.b.decompose()

		if(annotation.text is not None):
			annotation=annotation.text
	else:
		annotation = ""

	print("Nazev: "+Nazev+'\n')
	for genre in genres:
		print("Zanr: "+genre.text+'\n')
	print("Autor: "+author+'\n')
	print("Anotace: "+annotation.replace('\n',' ').replace(chr(13),'')+'\n')


def WebScrape_reviews(my_url):
	#otevre url a precte html zadaneho url
	my_url=my_url.encode('utf-8').decode('ascii', 'ignore')
	try:
		uClient = uReq(my_url)
	except urllib.error.HTTPError:
		return
	page_html = uClient.read()
	uClient.close()

	#vyhledani hledanych dat v html
	page_soup = soup(page_html, "html.parser")
	Nazev = page_soup.h1.text

	#tisk vyhledanych dat
	NazevDir = Nazev.translate({ord(i): None for i in '"\/:|<>*?'})

	Webscrape_head(page_soup)
		

	#pocet stranek recenzi
	review_page_count=len(page_soup.findAll("a",{"class":"textlist_item_select_width round_mini"}))+1

	for review_page in range(1,review_page_count+1):
		if(review_page != 1):
			#zmena url a precteni
			my_url=my_url+'&comments_page='+str(review_page)
			#vyhledani recenzi v html
			uClient = uReq(my_url)
			page_html = uClient.read()
			uClient.close()
			page_soup = soup(page_html, "html.parser")
		reviews = page_soup.findAll("div",{"class":"comment"})

		for review in reviews:
			username=review.div.img["alt"]
			userid=review.a["href"].split('-')[1]

			header=review.find("div",{"class":"comment_header"})

			rating=header.img 
			if(rating is not None): #pripad kde recenze nema hodnoceni
				rating=header.img["alt"] 
			else:
				rating="??"

			date=header.find("span",{"class":"date_span"}).text
			comment=review.find("div",{"class":"comment_content"}).text
			comment=comment.replace('\n',' ').replace(chr(13),'')

			print(username+'\t'+userid+'\t'+date+'\t'+rating+'\t'+comment+'\n') 
		




my_url='https://www.cbdb.cz/kniha-163943-vek-slasti'

WebScrape_reviews(my_url)