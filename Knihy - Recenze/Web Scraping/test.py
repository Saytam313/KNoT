from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import sys, datetime

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

# parallel-ssh -i -A -h Hosts python3 /mnt/minerva1/nlp/projects/sentiment9/Scripts/test.py  \$HOSTNAME
my_url='https://www.databazeknih.cz/knihy/posledni-prani-30396'
#otevre url a precte html zadaneho url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#vyhledani hledanych dat v html
page_soup = soup(page_html, "html.parser")

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
		
		comment=review.div.p.text.replace('\n','')

		print(username+'\t'+str(likes)+'\t'+str(date)+'\t'+str(rating)+'\t'+comment+'\n') 
