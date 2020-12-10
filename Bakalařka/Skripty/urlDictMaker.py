def readURLs(link):
	datafile=open(link,"r",encoding="utf8")
	dataContent=datafile.read()
	for x in dataContent.splitlines():
		if(x.startswith('#stopper#')):
			continue

		UrlPartList=x.split('/')[3:]
		
		#print(UrlPartList)
		UrlPartList.reverse()
		#ReverseList=UrlPartList.reverse()
		
		#print(UrlPartList)
		#UrlLongestPart=sorted(UrlPartList,key=len)[-1]
		WordWeight=0
		for part in UrlPartList:
			UrlPartWords=part.split('-')
			if(WordWeight<3):
				WordWeight+=1
			for word in UrlPartWords:
				if('#comment' in word):
					word=word.split('#comment')[0]
				if(word not in AllWordCounter.keys()):
					AllWordCounter[word]=WordWeight
				else:
					AllWordCounter[word]+=WordWeight















AllWordCounter=dict()
readURLs('..\Data\\ReviewUrls.txt')
print(sorted(AllWordCounter.items(), key=lambda j: j[1]))