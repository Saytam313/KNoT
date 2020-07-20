from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    

my_url='https://www.cbdb.cz/kniha-195063-10-celostatni-konference-o-predpjatem-betonu?order_comments=time'

#otevre url a precte html zadaneho url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

#vyhledani hledanych dat v html
page_soup = soup(page_html, "html.parser")
genres = page_soup.findAll("span",{"itemprop":"genre"})
author = page_soup.find("a",{"itemprop":"author"}).text
annotation = page_soup.find("div",{"id":"book_annotation"})
annotation.b.decompose()


#tisk vyhledanych dat
print("Nazev: ",page_soup.h1.text)
for genre in genres:
	print("Zanr: ",genre.text)
print("Autor: ",author)
print("Anotace: ",annotation.text)
#pocet stranek recenzi
rewiev_page_count=len(page_soup.findAll("a",{"class":"textlist_item_select_width round_mini"}))+1

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
		print(str(rewiev_cnt)+'\t'+username+'\t'+userid+'\t'+date+'\t'+rating+'\t'+comment+'\n') 

print("pocet recenzi",rewiev_cnt)
if(rewiev_cnt>0):
	print("prumerne hodnoceni",str(round((rewiev_rating_sum/rewiev_cnt),2))+'%')