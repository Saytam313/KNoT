from bs4 import BeautifulSoup as soup 
import os
import brandFinder

def FindReviews(link):

	URLsubstringlist=["recenze","hodnoceni"]

	
	datafile=open(link,"r",encoding="utf8")
	dataContent=datafile.read()
	dataContentList=dataContent.split('WARC/1.0')[2:]
	#writeFile=open("urls.txt",'w')
	cnter=0
	for x in dataContentList:

		page_soup = soup(x, "html.parser")
		for j in page_soup.findAll("h1"):
			print(j.text)
		exit()
		for line in x.splitlines():
			if("WARC-Target-URI:" in line):

				url=line.replace("\n","").split('WARC-Target-URI: ')[1]
				
				if(url.startswith('https://www.autojournal.cz/test')):
					print(url)
				elif(url.startswith('https://autoroad.cz/testy-aut/')):
					print(url)
				elif(url.startswith('https://smartmania.cz/test')): #pridat ignorovani komentaru
					url_split=url.split('/')
					if('comment' in url_split[-1]):
						continue
					else:
						print(url)
				elif(url.startswith('https://auto-mania.cz/test')):
					print(url)	
				
				elif(url.startswith('https://vybermiauto.cz/recenze/')):
					print(url)


def readReviews(link):
	reviewWordsList=["recenze"]
	reviewWordsList = reviewWordsList+brands
	
	reviewWordsList=[x.lower() for x in reviewWordsList]
	datafile=open(link,"r",encoding="utf8")
	ReviewUrlsFile=open('..\Data\\ReviewUrls.txt',"r",encoding="utf8")
	ReviewUrlsText=ReviewUrlsFile.read()
	ReviewUrlsList=ReviewUrlsText.splitlines()

	dataContent=datafile.read()
	dataContentList=dataContent.split('<doc')
	#AllWordCounter=dict()

	goodWords=list()

	for x in dataContentList:
		firstLine=True
		WordResult=0
		UrlResult=0
		url=''
		LinkInPar=False
		ParagraphLines=list()
		for line in x.splitlines():


			if(firstLine==True):
				firstLine=False
				url=line.split('url="')[-1].split('"')[0]
				if('comment' in url.split('#')[-1]):
					break
				UrlResult=readURL(url)
			#if(line.startswith('<p')):

			ParagraphLines.append(line)
			if(line.startswith('<link')):
				LinkInPar=True
			if(line.startswith('</p')):
				if(not LinkInPar):
					for ParagraphLine in ParagraphLines:
						print(ParagraphLine)
						if(ParagraphLine in reviewWordsList):
							WordResult+=1
							goodWords.append(line)
				LinkInPar=False
				ParagraphLines=list()
		Result=UrlResult*5+WordResult
		if(Result>=6):
			print(url,': ',Result)
			print('Word: ',WordResult,'|Url: ', UrlResult)
			print(goodWords)
			goodWords=list()


	'''Vyhledavani slov ktery se vyskytuji ve clancich bez recenzi
		if(url not in ReviewUrlsList):
			if(not line.startswith('<')):
				print(line)
				if(line not in AllWordCounter.keys()):
					AllWordCounter[line]=1
				else:
					AllWordCounter[line]+=1
		'''
	#print(sorted(AllWordCounter.items(), key=lambda j: j[1]))
def readURL(url):

	goodWords=['test','recenze']
	goodWords.append(brands)
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
#f = open('asd.txt','w')
reviewProduct='auto'
AllWordCounter=dict()
brands=brandFinder.findBrands(reviewProduct)
#for x in os.listdir('..\Data\\vert\\'):
	#FindReviews('..\Data\\'+x)
#	readReviews('..\Data\\vert\\'+x)
readReviews('..\Data\\vert\\2020-09-10_0035.vert.processing')
#print(sorted(AllWordCounter.items(), key=lambda j: j[1]))

#FindReviews('..\Data\\2020-10-20_0224.warc.failed')
