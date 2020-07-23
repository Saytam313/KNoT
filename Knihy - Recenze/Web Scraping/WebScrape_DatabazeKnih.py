from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys


my_url='https://www.databazeknih.cz/knihy/harry-potter-harry-potter-a-fenixuv-rad-13?str=1'

#otevre url a precte html zadaneho url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#vyhledani hledanych dat v html
page_soup = soup(page_html, "html.parser")

Nazev = page_soup.find("h1",{"itemprop":"name"}).text

BookDirPath="../Results/"+Nazev
if(not os.path.isdir(BookDirPath)):
	os.mkdir("../Results/"+Nazev);

DatabazeKnihReviews = open("../Results/"+Nazev+"/DatabazeKnihReviews.txt", "w",encoding="utf-8")


#pocet stranek recenzi protoze prvni stranka je otevrena s prvnim pristupem na url
rewiev_page_count=int(page_soup.find("div",{"class":"pager"}).text.split(' ')[-1])



rewiev_cnt=0
rewiev_rating_sum=0
for rewiev_page in range(1,rewiev_page_count+1):
	if(rewiev_page != 1):
		#zmena url a precteni
		my_url=my_url+'&str='+str(rewiev_page)
		#vyhledani recenzi v html
		uClient = uReq(my_url)
		page_html = uClient.read()
		uClient.close()
		page_soup = soup(page_html, "html.parser")
	reviews = page_soup.findAll("div",{"class":"komentars_user komover"})
	
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
		else:
			date='??'

		rating=review.div.div.img
		if(rating is not None):
			rating=rating["src"][:-4]
			rating=int(rating[-1])*20
		else:
			rating='??'
		
		comment=review.div.p.text.replace('\n','')
		rewiev_cnt+=1
		if(rating != '??'): #pokud uzivatel neudal hvezdickove hodnoceni, je zapocteno prumerne hodnoceni 50

			rewiev_rating_sum+=int(rating)
		else:
			rewiev_rating_sum+=50 

		DatabazeKnihReviews.write(username+'\t'+str(likes)+'\t'+date+'\t'+str(rating)+'\t'+comment+'\n') 


#print("pocet recenzi",rewiev_cnt)
#print("prumerne hodnoceni",str(round((rewiev_rating_sum/rewiev_cnt),2))+'%')

bookInfo = open("../Results/"+Nazev+"/BookInfo.txt", "a",encoding="utf-8")


bookInfo.write("DatabazeKnih - pocet recenzi: "+str(rewiev_cnt)+'\n')
if(rewiev_cnt>0):
	bookInfo.write("DatabazeKnih - prumerne hodnoceni: "+str(round((rewiev_rating_sum/rewiev_cnt),2))+'%'+'\n')

bookInfo.close()

DatabazeKnihReviews.close()