from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys

def Webscrape_head(page_soup):
	Nazev = page_soup.h1.text
	NazevDir = Nazev.translate({ord(i): None for i in '"\/:|<>*?'})
	BookInfoFile=open("../Results/"+NazevDir+"/BookInfo.txt", "w",encoding="utf-8")

	author = page_soup.find("a",{"itemprop":"author"}).text
	genres = page_soup.findAll("span",{"itemprop":"genre"})
	annotation = page_soup.find("div",{"id":"book_annotation"})
	annotation.b.decompose()

	BookInfoFile.write("Nazev: "+Nazev+'\n')
	for genre in genres:
		BookInfoFile.write("Zanr: "+genre.text+'\n')
	BookInfoFile.write("Autor: "+author+'\n')
	BookInfoFile.write("Anotace: "+annotation.text+'\n')
	BookInfoFile.close()


def WebScrape_reviews(my_url):
	#otevre url a precte html zadaneho url
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	#vyhledani hledanych dat v html
	page_soup = soup(page_html, "html.parser")
	Nazev = page_soup.h1.text

	#tisk vyhledanych dat
	NazevDir = Nazev.translate({ord(i): None for i in '"\/:|<>*?'})
	BookDirPath="../Results/"+NazevDir
	if(not os.path.isdir(BookDirPath)):
		os.mkdir("../Results/"+NazevDir);


	if('BookInfo.txt' not in os.listdir("../Results/"+NazevDir)):
		Webscrape_head(page_soup)
		

	#pocet stranek recenzi
	rewiev_page_count=len(page_soup.findAll("a",{"class":"textlist_item_select_width round_mini"}))+1

	if(os.path.exists("../Results/"+NazevDir+"/cbdbReviews.txt")):
		cbdbReviews = open("../Results/"+NazevDir+"/cbdbReviews.txt", "a",encoding="utf-8")		
	else:
		cbdbReviews = open("../Results/"+NazevDir+"/cbdbReviews.txt", "w",encoding="utf-8")

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
			cbdbReviews.write(username+'\t'+userid+'\t'+date+'\t'+rating+'\t'+comment+'\n') 

	bookInfo = open("../Results/"+NazevDir+"/BookInfo.txt", "a",encoding="utf-8")


	bookInfo.write("cbdb - pocet recenzi: "+str(rewiev_cnt)+'\n')
	if(rewiev_cnt>0):
		bookInfo.write("cbdb - prumerne hodnoceni: "+str(round((rewiev_rating_sum/rewiev_cnt),2))+'%'+'\n')

	bookInfo.close()
	cbdbReviews.close()