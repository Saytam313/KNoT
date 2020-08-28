from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys
import datetime
import WebScrape_cbdb

def get_date(Datestr):
	return datetime.datetime.strptime(Datestr, '%d. %m. %Y, %H:%M')


NewReviewsFile = open("/mnt/minerva1/nlp/projects/sentiment9/Results/cbdbNewReviews.txt", "r",encoding="utf-8")
NewReviewBooks=NewReviewsFile.read().splitlines()

LastUpdateDate = get_date(NewReviewBooks[0])
NewReviewBooks.pop(0)#odstraneni data posledni aktualizace ze seznamu

for line in NewReviewBooks:
	
	my_url='https://www.cbdb.cz/'+line+'?order_comments=time'
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	reviews = page_soup.findAll("div",{"class":"comment"})

	Nazev = page_soup.h1.text

	#WebScrape_cbdb.Webscrape_head(page_soup)


	cbdbReviews = open("/mnt/minerva1/nlp/projects/sentiment9/Results/Reviews.tsv", "a",encoding="utf-8")
	rewiev_page_count=len(page_soup.findAll("a",{"class":"textlist_item_select_width round_mini"}))+1	

	for rewiev_page in range(1,rewiev_page_count+1):

		if(rewiev_page!=1):
			my_url='https://www.cbdb.cz/'+line+'?order_comments=time'+'?comments_page='+str(rewiev_page)

			uClient = uReq(my_url)
			page_html = uClient.read()
			uClient.close()
			page_soup = soup(page_html, "html.parser")
		reviews = page_soup.findAll("div",{"class":"comment"})

		for review in reviews:
			username=review.div.img["alt"]
			userid=review.a["href"].split('-')[1]

			header=review.find("div",{"class":"comment_header"})
			date=header.find("span",{"class":"date_span"}).text

			if(get_date(date) < LastUpdateDate):
				break

			rating=header.img 
			if(rating is not None): #pripad kde recenze nema hodnoceni
				rating=header.img["alt"] 
			else:
				rating="??"

			comment=review.find("div",{"class":"comment_content"}).text

			cbdbReviews.write("cbdb"+'\t'+Nazev+'\t'+username+'\t'+userid+'\t'+date+'\t'+rating+'\t'+comment.replace('\n',' ').replace(chr(13),'').replace('  ','').strip()+'\n') 



NewReviewsFile.close()

NewReviewsFile = open("/mnt/minerva1/nlp/projects/sentiment9/Results/cbdbNewReviews.txt", "w",encoding="utf-8")
NewReviewsFile.write(str(datetime.datetime.now().strftime("%d. %m. %Y, %H:%M"))+'\n')

NewReviewsFile.close()