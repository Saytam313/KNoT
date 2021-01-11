from bs4 import BeautifulSoup as soup 
from difflib import SequenceMatcher
import os
import brandFinder

reviewProduct='auto'
brands=brandFinder.findBrands(reviewProduct)
product=brandFinder.findProductNames(reviewProduct)

def SubstrInList(word,list):
	if(len(word)>1):
		if(word[0].islower() and len(word)<4):#specialni priklad po porovnavani znacek, nektery znacky jsou kratky treba BMW
			return False
	else:
		return False
	#s = SequenceMatcher(None,"notebook","laptop")

	for x in list:
		
		if(word in x):
			return True
		elif(x in word):
			return True
	return False

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
	reviewWordsListPart = ['recenze','test']
	#reviewWordsListPart.append(reviewProduct)
	#reviewWordsListFull = reviewWordsListPart+brands

	
	#reviewWordsListFull=[x.lower() for x in reviewWordsListFull]
	datafile=open(link,"r",encoding="utf8")
	ReviewUrlsFile=open('..\Data\\ReviewUrls.txt',"r",encoding="utf8")
	ReviewUrlsText=ReviewUrlsFile.read()
	ReviewUrlsList=ReviewUrlsText.splitlines()

	dataContent=datafile.read()
	dataContentList=dataContent.split('<doc')
	#AllWordCounter=dict()


	for x in dataContentList:
		firstLine=True
		WordResult=0
		UrlResult=0
		
		IsReview=0
		IsProduct=0
		IsBrand=0



		url=''
		LinkInPar=False
		ParagraphLines=list()
		for line in x.splitlines():


			if(firstLine==True):
				#print('\n\n\n\n\n\n\n')
				firstLine=False
				url=line.split('url="')[-1].split('"')[0]
				if('comment' in url.split('#')[-1]):
					break
				UrlResult=readURL(url)


				IsReview=0
				IsProduct=0
				IsBrand=0
			#if(line.startswith('<p')):

			ParagraphLines.append(line)
			if(line.startswith('<link')):
				LinkInPar=True
			if(line.startswith('</p')):
				if(not LinkInPar):
					paragraph=list()
					for ParagraphLine in ParagraphLines:
						if(not ParagraphLine.startswith('<')):
							paragraph.append(ParagraphLine)
							if(SubstrInList(ParagraphLine,reviewWordsListPart)):
								WordResult+=100
								IsReview+=1
								#print('\t\t\t\t\t\t',ParagraphLine)
							
							
							if(SubstrInList(ParagraphLine,brands)):
							#if(ParagraphLine in reviewWordsList):
								#print('WOR: ',ParagraphLine)
								WordResult+=1
								IsBrand+=1
								#print(ParagraphLine)
							


							if(SubstrInList(ParagraphLine,product)):
							#if(ParagraphLine in reviewWordsList):
								#print('WOR: ',ParagraphLine)
								WordResult+=20
								IsProduct+=1
								#print(ParagraphLine)
					#print(' '.join(paragraph),'.')
				LinkInPar=False
				ParagraphLines=list()
		Result=UrlResult*1+WordResult

		if(IsReview>0):
			if(IsProduct>5):
				if(IsBrand+IsProduct*2>49):

					print('\n\t\t\t',url,': ',end='')
				else:
					print('\n',url,': ',end='')
				print('Review: ',IsReview,end=' ')
				print('Product: ',IsProduct,end=' ')
				print('Brand: ',IsBrand,end=' ')
				print('P+B: ',IsBrand+IsProduct*2,end=' ')
			
			#if(IsBrand>0):
				#print('Brand: ',IsBrand,end=' ')
		'''
		if(Result>100):
			print(url,': ',Result)
			print('Word: ',WordResult,'|Url: ', UrlResult)
			#break
		'''

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


	reviewWordsListPart = ['test','recenze']
	reviewWordsListPart.append(reviewProduct)
	#reviewWordsListFull = reviewWordsListPart+brands

	
	#reviewWordsListFull=[x.lower() for x in reviewWordsListFull]


	UrlPartList=url.split('/')[3:]#odstraneni protokolu a webu z url
	
	UrlPartList.reverse()
	#ReverseList=UrlPartList.reverse()
	
	#print(UrlPartList)
	#UrlLongestPart=sorted(UrlPartList,key=len)[-1]
	WordWeight=1
	Result=0
	for part in UrlPartList:
		UrlPartWords=part.split('-')
		
		if(WordWeight<3):
			WordWeight+=1
		for word in UrlPartWords:
			if(SubstrInList(word,reviewWordsListPart)):
				Result+=100
			'''	
			if(SubstrInList(word,brands)):
				Result+=1
			'''
			if(SubstrInList(word,product)):
				Result+=1
			#if(word in reviewWordsListFull):
				#print('URL: ',word)
				#Result+=WordWeight
	return Result
def readSpecificURL(link,SpecURL):
	reviewWordsListPart = ['recenze','test']
	#reviewWordsListPart.append(reviewProduct)
	#reviewWordsListFull = reviewWordsListPart+brands

	
	#reviewWordsListFull=[x.lower() for x in reviewWordsListFull]
	datafile=open(link,"r",encoding="utf8")
	#ReviewUrlsFile=open('..\Data\\ReviewUrls.txt',"r",encoding="utf8")
	#ReviewUrlsText=ReviewUrlsFile.read()
	#ReviewUrlsList=ReviewUrlsText.splitlines()

	dataContent=datafile.read()
	dataContentList=dataContent.split('<doc')
	#AllWordCounter=dict()


	for x in dataContentList:
		firstLine=True
		WordResult=0
		UrlResult=0
		
		IsReview=0
		IsProduct=0
		IsBrand=0



		url=''
		LinkInPar=False
		ParagraphLines=list()
		for line in x.splitlines():


			if(firstLine==True):
				#print('\n\n\n\n\n\n\n')
				firstLine=False
				url=line.split('url="')[-1].split('"')[0]
				if('comment' in url.split('#')[-1]):
					break
				if(url!=SpecURL):
					break
				UrlResult=readURL(url)


				IsReview=0
				IsProduct=0
				IsBrand=0
			#if(line.startswith('<p')):

			ParagraphLines.append(line)
			if(line.startswith('<link')):
				LinkInPar=True
			if(line.startswith('</p')):
				if(not LinkInPar):
					paragraph=list()
					for ParagraphLine in ParagraphLines:
						if(not ParagraphLine.startswith('<')):
							paragraph.append(ParagraphLine)
							if(SubstrInList(ParagraphLine,reviewWordsListPart)):
								WordResult+=100
								IsReview+=1
								#print('\t\t\t\t\t\t',ParagraphLine)
							
							
							if(SubstrInList(ParagraphLine,brands)):
							#if(ParagraphLine in reviewWordsList):
								#print('WOR: ',ParagraphLine)
								WordResult+=1
								IsBrand+=1
								#print(ParagraphLine)
							


							if(SubstrInList(ParagraphLine,product)):
							#if(ParagraphLine in reviewWordsList):
								#print('WOR: ',ParagraphLine)
								WordResult+=20
								IsProduct+=1
								#print(ParagraphLine)
					print(' '.join(paragraph),'.')
				LinkInPar=False
				ParagraphLines=list()
		Result=UrlResult*1+WordResult

		if(IsReview>0):
			'''
			if(IsProduct>5):
				if(IsBrand+IsProduct*2>49):

					print('\n\t\t\t',url,': ',end='')
				else:
					print('\n',url,': ',end='')
				print('Review: ',IsReview,end=' ')
				print('Product: ',IsProduct,end=' ')
				print('Brand: ',IsBrand,end=' ')
				print('P+B: ',IsBrand+IsProduct*2,end=' ')
			
			'''
			print('\n',url,end='')	


#f = open('asd.txt','w')

AllWordCounter=dict()
#print(product)
#print(brands)
for x in os.listdir('..\Data\\vert\\'):
	#FindReviews('..\Data\\'+x)
	readReviews('..\Data\\vert\\'+x)

#readReviews('..\\testClanek.txt')

#readReviews('..\Data\\vert\\2020-09-10_0035.vert.processing')
#readSpecificURL('..\Data\\vert\\2020-09-10_0035.vert.processing','https://www.topspeed.sk/novinky/vw-golf-variant-2021-oficialne-prekvapil-dlhsim-razvorom-aj-verziou-alltrack/18277')

#print(sorted(AllWordCounter.items(), key=lambda j: j[1]))

#FindReviews('..\Data\\2020-10-20_0224.warc.failed')
