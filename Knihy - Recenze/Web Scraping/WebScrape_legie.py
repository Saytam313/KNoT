from urllib.request import urlopen as uReq
import urllib
from bs4 import BeautifulSoup as soup    
import os, sys, time, re
from datetime import datetime
def get_date(datestr):
	FormatedDate=datetime.strptime(datestr, "%d.%m.%Y %H:%M")

	return datetime.strftime(FormatedDate,"%Y-%m-%d %H:%M:%S")
	#2020-08-27 12:45:34.775521
#29.05.2008 08:35

def WebScrape(my_url):
#my_url='https://www.legie.info/kniha/20123-klara-mayerova-a-pak-ho-spolknul-eskalator'.encode('utf-8').decode('ascii', 'ignore')
#my_url='https://www.legie.info/kniha/220-joanne-kathleen-rowling-harry-potter-a-kamen-mudrcu'.encode('utf-8').decode('ascii', 'ignore')
#my_url='https://www.legie.info/kniha/12431-alan-vanneman-sherlock-holmes-a-obri-krysa-ze-sumatry'.encode('utf-8').decode('ascii', 'ignore')
	my_url=my_url.encode('utf-8').decode('ascii', 'ignore')


	try:
		uClient = uReq(my_url)
	except:
		exit()


	page_html = uClient.read()
	uClient.close()

	#vyhledani hledanych dat v html
	page_soup = soup(page_html, "html.parser")

	nazev=page_soup.find("h2",{"id":"nazev_knihy"}).text

	autor=page_soup.h3.a.text 

	anotace=page_soup.find("div",{"id":"nic"})
	if(anotace is None):
	#	anotace=page_soup.find("div",{"id":"anotace"}).p.text
		anotace=page_soup.find("div",{"id":"anotace"})
		anotaceStr=""
		for x in anotace:
			strX=str(x)
			if('<p>' in strX):
				#print(x.text)
				anotaceStr+=x.text
			elif('<hr/>' in strX):
				break
	else:
		anotaceStr=anotace.p.text

	zalozky=page_soup.find("ul",{"id":"zalozky"})

	print('legie.info'+'\t'+nazev+'\t'+autor+'\t'+anotaceStr.replace('\n',' ').replace(chr(13),'').replace('  ','').strip())

	for x in zalozky:
		if("komentare" in str(x)):
			komentareStr=x.text
			komentareCnt=int(re.search('#(.*)\)',komentareStr).groups()[0])
			if(komentareCnt>0):
				my_url=my_url+'/komentare#zalozky'
				#my_url='https://www.legie.info/kniha/220-harry-potter-a-kamen-mudrcu/komentare#zalozky'
				uClient = uReq(my_url)
				page_html = uClient.read()
				uClient.close()
				page_soup = soup(page_html, "html.parser")

				Komentare = page_soup.findAll("div",{"class":"komentar okraj"})
				for koment in Komentare:
					autor=koment.a.text
					hodnoceniStr=koment.find("div",{"class":"nick_a_hodnoceni"}).a.next_sibling.replace('|','').strip()
					hodnoceni=0
					if(hodnoceniStr=='nehodnoceno'):
						hodnoceni='??'
					elif(hodnoceniStr=='brak'):
						hodnoceni=0
					else:
						if('1/2' in hodnoceniStr):
							hodnoceniStr=hodnoceniStr.replace('1/2','')
							hodnoceni=10
						hodnoceni+=len(hodnoceniStr)*20

					datum=koment.span.text
					text=koment.p.text
					print(autor+'\t'+str(hodnoceni)+'\t'+get_date(datum)+'\t'+text.replace('\n',' ').replace(chr(13),'').replace('  ','').strip())



