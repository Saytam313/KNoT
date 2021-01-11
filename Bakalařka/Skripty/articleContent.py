def readReviews(link,inputurl):
	reviewWordsListPart = ['recenze']

	datafile=open(link,"r",encoding="utf8")

	dataContent=datafile.read()
	dataContentList=dataContent.split('<doc')
	cnt=0
	resultDict=dict()
	for x in dataContentList:
		#print('\n\n====================================\n\n')
		#if(cnt>5):
		#	break
		#cnt+=1
		firstLine=True
		WordResult=0
		UrlResult=0
		
		IsReview=0
		IsProduct=0
		IsBrand=0



		url=''
		LinkInPar=False
		ParagraphLines=list()
		par=list()
		for line in x.splitlines():


			if(firstLine==True):
				firstLine=False
				url=line.split('url="')[-1].split('"')[0]
				
				if('comment' in url.split('#')[-1] or '.sk' in url):
					break
			if(url==inputurl):
				lineList=line.split('\t')
				print(line)
					#print(lineList[1])
				ParagraphLines.append(line)
				if(line.startswith('<link')):
					LinkInPar=True
				if(line.startswith('</p')):
					if(not LinkInPar):
						paragraph=list()
						for ParagraphLine in ParagraphLines:
							if(not ParagraphLine.startswith('<')):
									
									paragraph.append(ParagraphLine)

									#print(ParagraphLine)

readReviews('..\Data\parsed\\2019-01-25_0215.parsed','https://www.svetandroida.cz/fortnite-prani-spinavych-penez/')