from urllib.request import urlopen as uReq
import urllib
from bs4 import BeautifulSoup as soup    
import os, sys, time
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def WebScrape_novinky(url):
	try:
		uClient = uReq(url)
	except:
		return


	page_html = uClient.read()
	#print(page_html)
	uClient.close()

	#vyhledani hledanych dat v html
	page_soup = soup(page_html, "html.parser")
	#print(page_soup)
	#pocet stranek recenzi
	#product_list=page_soup.findAll("div",{"class":"product"})
	#print(page_soup.findAll("div",{"class":"product"})[0].h2.text)
	OriginalHead=page_soup.find("div",{"class":"f_eF f_eH"}).select("td")[0].text
	print(OriginalHead)

def WebScrape_idnes(url):

	uClient = uReq(url)
	page_html = uClient.read()
	#print(page_html)
	uClient.close()
	page_soup = soup(page_html, "html.parser")

	print(page_soup.findAll("h3",{"itemprop":"name"})[0].text)

def WebScrape_lidovky(url):

	uClient = uReq(url)
	page_html = uClient.read()
	#print(page_html)
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	print(page_soup.find("table",{"class","complete not4bbtext"}).find('span').text)

	#print(page_soup.findAll("h3",{"itemprop":"name"})[0].text)
def WebScrape_aktualne(url):

	uClient = uReq(url)
	page_html = uClient.read()
	#print(page_html)
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	print(page_soup.findAll("div",{"class":"infobox"}).text)

def WebScrape_productAuto(product):

	search_word=product
	search_word=search_word.replace(' ','+')
	try:
		uClient = uReq('https://auto-mania.cz/?s='+search_word)
		#print('https://auto-mania.cz/?s='+search_word)
	except:
		return

	page_html = uClient.read()
	#print(page_html)
	uClient.close()

	#vyhledani hledanych dat v html
	page_soup = soup(page_html, "html.parser")

	#print(page_soup)
	#pocet stranek recenzi
	#product_list=page_soup.findAll("div",{"class":"product"})
	#print(page_soup.findAll("div",{"class":"product"})[0].h2.text)
	count=0
	#print(page_soup.findAll("div",{"ud":"td-outer-wrap"}))
	for x in page_soup.findAll("h3",{"class":"entry-title td-module-title"}):

		#print(x.h2.text)
		count+=1
		#print(product)
		#print(x.h2.text.lower())
		#print(similar(product,x.h2.text.lower()))
		#print(x.a.text.lower())
		if(similar(product,x.a.text.lower())>=0.3):
			return True
		if(count>5):
			break
	return False
	'''
	count=0
	for x in page_soup.findAll("div",{"class":"product"}):
		#print(x.h2.text)
		count+=1
		#print(product)
		#print(x.h2.text.lower())
		#print(similar(product,x.h2.text.lower()))
		if(similar(product,x.h2.text.lower())>=0.5):
			print(x.h2.text)
			return True
		if(count>4):
			return
	return False
	'''
'''
	for product in range(1,product_count+1):
		productName = page_soup.findAll("div",{"class":"comment"})

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

			cbdbReviews.write("cbdb"+'\t'+Nazev+'\t'+username+'\t'+userid+'\t'+date+'\t'+rating+'\t'+comment.replace('\n',' ').replace(chr(13),'').replace('  ','').strip()+'\n') 
		
		time.sleep(2)#delay mezi pristupy na stranky recenzí
	time.sleep(2)#delay mezi pristupy na knihy
'''


#search_word='redmi note 7'
#search_word=search_word.replace(' ','%20')
#search_word=search_word.replace(' ','+')

#print(similar('redmi note 7','redmi note 8'))

#WebScrape_product('A Potom')
#print(WebScrape_product('A Potom'))
#WebScrape_reviews('https://www.zbozi.cz/hledani/?q='+search_word)
#WebScrape_reviews('https://www.heureka.cz/?h%5Bfraze%5D='+search_word)
#WebScrape('https://www.idnes.cz/kultura/literatura/recenze-milan-kundera-slavnost-bezvyznamnosti.A200910_570074_literatura_spm#utm_source=rss&amp;utm_medium=feed&amp;utm_campaign=idnes&amp;utm_content=main')
#WebScrape_novinky('https://www.novinky.cz/kultura/clanek/recenze-dvorske-intriky-zbavene-romantiky-40268895 ')
#WebScrape_idnes('https://www.idnes.cz/kultura/film-televize/recenze-binoche-kdo-si-myslis-ze-jsem.A200914_570768_filmvideo_spm#utm_source=rss&amp;utm_medium=feed&amp;utm_campaign=idnes&amp;utm_content=main')
#WebScrape_lidovky('https://www.lidovky.cz/kultura/recenze-mezi-nami-sousedy-krajina-ve-stinu-ceka-v-kinech-na-ty-prave-divaky.A200909_214328_ln_kultura_jto#utm_source=rss&amp;utm_medium=feed&amp;utm_campaign=ln_lidovky&amp;utm_content=main')
#WebScrape_lidovky('https://magazin.aktualne.cz/kultura/film/favoritka-yorgos-lanthimos-film-oscar-nominace-recenze/r~215d71921ffa11e99d3cac1f6b220ee8/?utm_source=mediafed&utm_medium=rss&utm_campaign=mediafed')
WebScrape_productAuto('Peugeot 3008')