from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys
import datetime
import WebScrape_DatabazeKnih

NewReviewsFile = open("/mnt/minerva1/nlp/projects/sentiment9/Results/DatabazeKnihNewReviews.txt", "r",encoding="utf-8")
NewReviewBooks=NewReviewsFile.read().splitlines()

LastUpdateDate = WebScrape_DatabazeKnih.get_date(NewReviewBooks[0])
NewReviewBooks.pop(0)#odstraneni data posledni aktualizace ze seznamu

for line in NewReviewBooks:
	my_url='https://www.databazeknih.cz/'+line
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	reviews = page_soup.findAll("div",{"class":"komentars_user komover"})
	
	Nazev = page_soup.find("h1",{"itemprop":"name"}).text
	NazevDir = Nazev.translate({ord(i): None for i in '"\/:|<>*?'})#odstraneni znaku ktere windows nepovoluje v nazvu slozky
	BookDirPath="../Results/"+NazevDir
	if(not os.path.isdir(BookDirPath)):
		os.mkdir("../Results/"+NazevDir);
		WebScrape_DatabazeKnih.Webscrape_reviews(my_url)
		continue

	if('BookInfo.txt' not in os.listdir("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir)):
		WebScrape_DatabazeKnih.Webscrape_head(page_soup)

	DatabazeKnihReviews = open("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/DatabazeKnihReviews.txt", "a",encoding="utf-8")


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
			break

		rating=review.div.div.img
		if(rating is not None):
			rating=rating["src"][:-4]
			rating=int(rating[-1])*20
		else:
			rating='??'
		
		comment=review.div.p.text.replace('\n','')


		DatabazeKnihReviews.write(username+'\t'+str(date)+'\t'+str(rating)+'\t'+comment+'\n') 



NewReviewsFile.close()

NewReviewsFile = open("/mnt/minerva1/nlp/projects/sentiment9/Results/DatabazeKnihNewReviews.txt", "w",encoding="utf-8")
NewReviewsFile.write(str(datetime.datetime.now().strftime("%d. %m. %Y, %H:%M"))+'\n')

NewReviewsFile.close()