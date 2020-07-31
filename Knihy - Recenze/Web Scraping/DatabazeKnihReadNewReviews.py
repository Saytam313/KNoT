from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys
import datetime


def get_date(Datestr):
	DateList=Datestr.split('. ')
	if (len(DateList)==2):
		MonthNameDict = {	
		'ledna' : 1,
		'února' : 2,
		'března' : 3,
		'dubna' : 4,
		'května' : 5,
		'června' : 6,
		'července' : 7,
		'srpna' : 8,
		'září' : 9,
		'října' : 10,
		'listopadu' : 11,
		'prosince' : 12,
		}
		ConvertedDateStr=str(DateList[0])+'|'+str(MonthNameDict[DateList[1]])+'|'+str(datetime.datetime.now().year)
		return datetime.datetime.strptime(ConvertedDateStr,'%d|%m|%Y')
	elif(len(DateList)>2):
		if(len(Datestr.split(','))>0):
			return datetime.datetime.strptime(Datestr, '%d. %m. %Y, %H:%M')

	else:
		Today=datetime.datetime.now()
		DayNameDict = {

		'předevčírem':2,
		'včera':1,
		'dnes':0,
		}

		if(len(Datestr.split('.'))>1):
			return datetime.datetime.strptime(Datestr,'%d.%m.%Y')
		else:
			return datetime.datetime.now()-datetime.timedelta(days=DayNameDict[Datestr])

NewReviewsFile = open("../Results/DatabazeKnihNewReviews.txt", "r",encoding="utf-8")
NewReviewBooks=NewReviewsFile.read().splitlines()

LastUpdateDate = get_date(NewReviewBooks[0])
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

	DatabazeKnihReviews = open("../Results/"+NazevDir+"/DatabazeKnihReviews.txt", "a",encoding="utf-8")


	for review in reviews:
		'''
		username=review.div.img["alt"]
		userid=review.a["href"].split('-')[1]
		
		date=review.div.div.span
		if(get_date(date) < LastUpdateDate):
			break

		rating=header.img 
		if(rating is not None): #pripad kde recenze nema hodnoceni
			rating=header.img["alt"] 
		else:
			rating="??"

		comment=review.find("div",{"class":"comment_content"}).text
		comment=comment.replace('\n',' ')
		'''
		username=review.div.a.text

		likes=review.div.div.em
		if(likes is not None):
			likes=likes.text
		else:
			likes=0
		date=review.div.div.span
		if(date is not None):
			date=date.text
			date=get_date(date)
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

NewReviewsFile = open("../Results/DatabazeKnihNewReviews.txt", "w",encoding="utf-8")
NewReviewsFile.write(str(datetime.datetime.now().strftime("%d. %m. %Y, %H:%M"))+'\n')

NewReviewsFile.close()