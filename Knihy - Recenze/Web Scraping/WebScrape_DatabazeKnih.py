from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys, datetime, time

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

def Webscrape_head(page_soup):
	Nazev = page_soup.find("h1",{"itemprop":"name"}).text
	NazevDir = Nazev.translate({ord(i): None for i in '"\/:|<>*?'})#odstraneni znaku ktere windows nepovoluje v nazvu slozky
	BookInfoFile=open("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/BookInfo.txt", "w",encoding="utf-8")

	Autor = page_soup.find("span",{"itemprop":"author"}).text
	Zanry = page_soup.select('a[href*="zanr"]')

	try:
		AnotacePart1 = page_soup.find("span",{"class":"start_text"})
		if (AnotacePart1 is not None):
			AnotacePart1=AnotacePart1.text.replace(chr(13),'').replace('\n',' ')
			AnotacePart2 = page_soup.find("span",{"class":"end_text"})
			AnotacePart2=AnotacePart2.text.replace(chr(13),'').replace('\n',' ')
			Anotace = str(AnotacePart1)+str(AnotacePart2)
		else:
			Anotace = page_soup.find("p",{"id":"bdetdesc"}).text.replace(chr(13),'').replace('\n',' ')

	except AttributeError:
		Anotace = '??'

	BookInfoFile.write("Nazev: "+Nazev+'\n')
	for genre in Zanry:
		BookInfoFile.write("Zanr: "+genre.text+'\n')
	BookInfoFile.write("Autor: "+Autor+'\n')
	BookInfoFile.write("Anotace: "+Anotace+'\n')
	BookInfoFile.close()


def Webscrape_reviews(my_url):
	if('c=all' not in my_url):
		my_url = my_url + '?c=all'
	#otevre url a precte html zadaneho url
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	#vyhledani hledanych dat v html
	page_soup = soup(page_html, "html.parser")

	Nazev = page_soup.find("h1",{"itemprop":"name"}).text
	NazevDir = Nazev.translate({ord(i): None for i in '"\/:|<>*?'})#odstraneni znaku ktere windows nepovoluje v nazvu slozky

	BookDirPath="/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir
	if(not os.path.isdir(BookDirPath)):
		os.mkdir("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir);

	if('BookInfo.txt' not in os.listdir("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir)):
		Webscrape_head(page_soup)


	if(os.path.exists("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/DatabazeKnihReviews.txt")):
		DatabazeKnihReviews = open("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/DatabazeKnihReviews.txt", "a",encoding="utf-8")
	else:

		DatabazeKnihReviews = open("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/DatabazeKnihReviews.txt", "w",encoding="utf-8")





	rewiev_page_count=1
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
		reviews+= page_soup.findAll("div",{"class":"komentars_user_last komover"})
		for review in reviews:
			username=review.div.a.text

			likes=review.div.div.em
			if(likes is not None):
				likes=likes.text
			else:
				likes=0
			date=review.div.div.span
			if(date is not None):
				date=get_date(date.text)
			else:
				date='??'

			rating=review.div.div.img
			if(rating is not None):
				rating=rating["src"][:-4]
				rating=int(rating[-1])*20
			else:
				rating='??'
			
			comment=review.div.p.text.replace(chr(13),'').replace('\n',' ')

			DatabazeKnihReviews.write(username+'\t'+str(likes)+'\t'+str(date)+'\t'+str(rating)+'\t'+comment+'\n') 
		time.sleep(2)#delay mezi pristupy aby nespadl server

	bookInfo = open("/mnt/minerva1/nlp/projects/sentiment9/Results/"+NazevDir+"/BookInfo.txt", "a",encoding="utf-8")

	bookInfo.close()

	DatabazeKnihReviews.close()