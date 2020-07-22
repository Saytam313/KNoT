from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys

my_url='https://www.cbdb.cz/kniha-10-harry-potter-a-fenixuv-rad-harry-potter-and-the-order-of-the-phoenix?order_comments=time'

#otevre url a precte html zadaneho url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#vyhledani hledanych dat v html
page_soup = soup(page_html, "html.parser")
Nazev = page_soup.h1.text
genres = page_soup.findAll("span",{"itemprop":"genre"})
author = page_soup.find("a",{"itemprop":"author"}).text
annotation = page_soup.find("div",{"id":"book_annotation"})
annotation.b.decompose()

isbn=page_soup.find("span",{"itemprop":"isbn"}).text
if(isbn is None):
	isbn='??'

#tisk vyhledanych dat
BookDirPath="../Results/"+Nazev
if(not os.path.isdir(BookDirPath)):
	os.mkdir("../Results/"+Nazev);

bookInfo = open("../Results/"+Nazev+"/BookInfo.txt", "w",encoding="utf-8")


bookInfo.write("Nazev: "+Nazev+'\n')
for genre in genres:
	bookInfo.write("Zanr: "+genre.text+'\n')
bookInfo.write("Autor: "+author+'\n')
bookInfo.write("ISBN: "+isbn+'\n')
bookInfo.write("Anotace: "+annotation.text+'\n')
bookInfo.close()
#pocet stranek recenzi
rewiev_page_count=len(page_soup.findAll("a",{"class":"textlist_item_select_width round_mini"}))+1


cbdbReviews = open("../Results/"+Nazev+"/cbdbReviews.txt", "w",encoding="utf-8")

rewiev_cnt=0
rewiev_rating_sum=0
for rewiev_page in range(1,rewiev_page_count+1):
	if(rewiev_page != 1):
		#zmena url a precteni
		my_url=my_url+'&comments_page='+str(rewiev_page)
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
		comment=comment.replace('\n',' ')
		rewiev_cnt+=1
		if(rating!="??"):
			rewiev_rating_sum+=int(rating[:-1])
		cbdbReviews.write(str(rewiev_cnt)+'\t'+username+'\t'+userid+'\t'+date+'\t'+rating+'\t'+comment+'\n') 

#cbdbReviews.write("pocet recenzi: "+str(rewiev_cnt))
#if(rewiev_cnt>0):
	#cbdbReviews.write("prumerne hodnoceni: "+str(round((rewiev_rating_sum/rewiev_cnt),2))+'%')

cbdbReviews.close()