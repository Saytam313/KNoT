from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys, time
import datetime
import WebScrape_DatabazeKnih

NewReviewsFile = open("../Results/DatabazeKnihNewReviews.txt", "r",encoding="utf-8")
NewReviewBooks=NewReviewsFile.read().splitlines()

LastUpdateDate = WebScrape_DatabazeKnih.get_date(NewReviewBooks[0])
NewReviewBooks.pop(0)#odstraneni data posledni aktualizace ze seznamu

for line in NewReviewBooks:
	time.sleep(2)
	my_url='https://www.databazeknih.cz/'+line
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	reviews = page_soup.findAll("div",{"class":"komentars_user komover"})
	try:
		Nazev = page_soup.find("h1",{"itemprop":"name"}).text
	except AttributeError:
		continue
		
	DatabazeKnihReviews = open("../Results/Reviews.tsv", "a",encoding="utf-8")


	for review in reviews:
		username=review.div.a.text
		likes=review.div.div.em
		if(likes is not None):
			likes=likes.text
		else:
			likes=0
		date=review.div.div.span

		if(date is not None):
			date=date.text
			date=WebScrape_DatabazeKnih.get_date(date)
			if(date < LastUpdateDate):
				break
		else:
			date='??'

		rating=review.div.div.img
		if(rating is not None):
			rating=rating["src"][:-4]
			rating=int(rating[-1])*20
		else:
			rating='??'
		
		comment=review.div.p.text.replace(chr(13),'').replace('\n',' ')


		DatabazeKnihReviews.write("DatabazeKnih"+'\t'+Nazev+'\t'+username+'\t'+str(likes)+'\t'+str(date)+'\t'+str(rating)+'\t'+comment+'\n') 



NewReviewsFile.close()

NewReviewsFile = open("../Results/DatabazeKnihNewReviews.txt", "w",encoding="utf-8")
NewReviewsFile.write(str(datetime.datetime.now().strftime("%d. %m. %Y, %H:%M"))+'\n')

NewReviewsFile.close()