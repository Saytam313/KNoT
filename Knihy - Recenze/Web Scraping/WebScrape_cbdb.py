from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys, time

def Webscrape_head(page_soup):
	Nazev = page_soup.h1.text
	NazevDir = Nazev.translate({ord(i): None for i in '"\/:|<>*?'})
	BookInfoFile=open("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/BookInfo.txt", "w",encoding="utf-8")

	author = page_soup.find("a",{"itemprop":"author"}).text
	genres = page_soup.findAll("span",{"itemprop":"genre"})
	annotation = page_soup.find("div",{"id":"book_annotation"})
	if(annotation is not None):
		if(annotation.b is not None):
			annotation.b.decompose()

		if(annotation.text is not None):
			annotation=annotation.text
		else:
			annotation=""
	else:
		annotation = ""

	BookInfoFile.write("Nazev: "+Nazev+'\n')
	for genre in genres:
		BookInfoFile.write("Zanr: "+genre.text+'\n')
	BookInfoFile.write("Autor: "+author+'\n')
	BookInfoFile.write("Anotace: "+annotation.replace('\n',' ').replace(chr(13),'')+'\n')
	BookInfoFile.close()


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
	BookDirPath="/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir
	if(not os.path.isdir(BookDirPath)):
		os.mkdir("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir);
	else:
		return #odstranit 

	if('BookInfo.txt' not in os.listdir("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir)):
		Webscrape_head(page_soup)
		

	#pocet stranek recenzi
	review_page_count=len(page_soup.findAll("a",{"class":"textlist_item_select_width round_mini"}))+1

	if(os.path.exists("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/cbdbReviews.txt")):
		cbdbReviews = open("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/cbdbReviews.txt", "a",encoding="utf-8")		
	else:
		cbdbReviews = open("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/cbdbReviews.txt", "w",encoding="utf-8")


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

			cbdbReviews.write(username+'\t'+userid+'\t'+date+'\t'+rating+'\t'+comment+'\n') 
		
		time.sleep(2)#delay mezi pristupy aby nespadl server

	bookInfo = open("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/BookInfo.txt", "a",encoding="utf-8")

	bookInfo.close()
	cbdbReviews.close()