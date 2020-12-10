def readURL(url):

	goodWords=['test','recenze']
	UrlPartList=url.split('/')[3:]#odstraneni protokolu a webu z url
	
	UrlPartList.reverse()
	#ReverseList=UrlPartList.reverse()
	
	#print(UrlPartList)
	#UrlLongestPart=sorted(UrlPartList,key=len)[-1]
	WordWeight=0
	Result=0
	for part in UrlPartList:
		UrlPartWords=part.split('-')
		
		if(WordWeight<3):
			WordWeight+=1
		for word in UrlPartWords:
			if(word in goodWords):
				Result+=WordWeight
	return Result
			
AllWordCounter=dict()
UrlsFile=open("urls.txt","r",encoding="utf8")
UrlsText=UrlsFile.read()
for x in UrlsText.splitlines():
	score=readURL(x)
	if(score>0):
		print(x)
