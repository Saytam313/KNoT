from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup    
import os, sys

my_url='https://www.cbdb.cz/'

#otevre url a precte html zadaneho url
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

CommentArea = page_soup.find("div",{"id":"index_news2_comments_area"}) 
NewReviews=CommentArea.findAll("a",{"class":"index_news_photos"})

NewReviewsFile = open("/mnt/minerva1/nlp/projects/sentiment9/Results/cbdbNewReviews.txt", "r",encoding="utf-8")
ExistingReviews=NewReviewsFile.read().splitlines()

NewReviewsFile.close()

NewReviewsFile = open("/mnt/minerva1/nlp/projects/sentiment9/Results/cbdbNewReviews.txt", "a",encoding="utf-8")

for Review in NewReviews:
	ReviewBook=Review["href"].split('#')[0]
	if(ReviewBook not in ExistingReviews):
		NewReviewsFile.write(ReviewBook+'\n')




NewReviewsFile.close()

