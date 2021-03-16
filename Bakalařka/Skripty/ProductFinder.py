from urllib.request import urlopen as uReq
import urllib
from bs4 import BeautifulSoup as soup    
import os, sys, time
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def WebScrape_product(product):

	search_word=product
	search_word=search_word.replace(' ','+')
	try:
		uClient = uReq('https://www.heureka.cz/?h%5Bfraze%5D='+search_word)
	except:
		return

	time.sleep(2)
	#print('https://www.heureka.cz/?h%5Bfraze%5D='+search_word)
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
	#print(len(page_soup.findAll("div",{"class":"product"})))
	#print(page_soup)
	'''
	product_list=page_soup.findAll("div",{"class":"product"})
	if(len(product_list)==0):
		product_list=page_soup.findAll('a',{"class":"c-product__link"})
	'''
	product_list=page_soup.findAll('a',{"class":"c-product__link"})
	for x in product_list:
	#for x in page_soup.findAll("div",{"class":"product"}):
		#time.sleep(1)
		
		#print(x.h2.text)
		count+=1
		#print(product)
		#print(x.h2.text.lower())
		#print(similar(product.lower(),x.h2.text.lower()))
		#print(similar(product.lower(),x.text.lower()))
		#if(similar(product.lower(),x.h2.text.lower())>=0.3):
		if(similar(product.lower(),x.text.lower())>=0.3):
			return True
		if(count>2):
			break
	return False


def WebScrape_productAuto(product):

	search_word=product.strip()
	search_word=search_word.replace(' ','+')
	try:
		uClient = uReq('https://auto-mania.cz/?s='+search_word,timeout=10)
	except:
		return False
	try:
		page_html = uClient.read()
	except:
		return False
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
		if(count>3):
			break
	return False

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
#WebScrape_reviews('https://www.databazeknih.cz/knihy/sikmy-kostel-428618')
#WebScrape_productAuto('Renault Clio 30 Vznikl')
#print(WebScrape_product('Sony Xperia 1 II Tak '))