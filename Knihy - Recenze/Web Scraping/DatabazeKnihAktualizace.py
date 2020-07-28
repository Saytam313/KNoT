from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys

my_url='https://www.databazeknih.cz/nejnovejsi-komentare'

#otevre url a precte html zadaneho url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

NewReviews=page_soup.findAll("a",{"class":"new"})

NewReviewsFile = open("../Results/DatabazeKnihNewReviews.txt", "r",encoding="utf-8")
ExistingReviews=NewReviewsFile.read().splitlines()

NewReviewsFile.close()

NewReviewsFile = open("../Results/DatabazeKnihNewReviews.txt", "a",encoding="utf-8")

for Review in NewReviews:
	ReviewBook=Review["href"].split('#')[0]
	
	if(ReviewBook not in ExistingReviews):
		NewReviewsFile.write(ReviewBook+'\n')




NewReviewsFile.close()

