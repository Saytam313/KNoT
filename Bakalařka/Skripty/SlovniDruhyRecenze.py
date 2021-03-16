from urllib.request import urlopen as uReq
import urllib
from bs4 import BeautifulSoup as soup 
from difflib import SequenceMatcher
import os
import brandFinder
import ProductFinder
#product=['automobil', 'auto']
#brands=['GMC', 'Smart', 'Volkswagen Group', 'Ariès', 'Chrysler', 'automaker', 'Imperia', 'Balkania', 'Proton', 'Dongfeng Yueda Kia', 'Mahindra', 'Rover', 'Ford of Britain', 'SAIC Motor', 'Brilliance', 'Industries Mécaniques Maghrébines', 'Opel Eisenach', 'Heibao', 'Isotta Fraschini', 'Mastretta', 'MG Motor', 'Namco', 'Vector Motors', 'Nissan Motor Ibérica', 'Trnavské automobilové závody', 'UzAuto Motors', 'Volvo Cars', 'SsangYong', 'PSA', 'SEAT', 'AMC', 'Ariel Motor Company', 'Alpina', 'Maruti Suzuki', 'Société Automobiles Ménara', 'Subaru Corporation', 'Mazdaspeed', 'Chrysler Australia', 'Great Wall Motors', 'SCAT', 'Maybach', '9ff', 'World Auto', 'AMAG Automobil- und Motoren', 'BMC', 'DS', 'Mercedes-Benz India', 'Pak Suzuki Motors', 'Renault do Brasil', 'Saracakis', 'TCI', 'Volkswagen Group of America', 'Cupra', 'FCA Poland', 'Changan Ford Mazda', 'Scania', 'Hotai Motor', 'Suzuki Indomobil Motor', 'car designer', 'Takeoka', 'Ltd.', 'Zotye Auto', 'Zastava Special Automobiles', 'Mitchell', 'Toyota-Astra Motor', 'FMR', 'Cimos', 'FCA', 'General Motors of Canada', 'Società Torinese Automobili Rapid', 'Nismo', 'Metro Cammell Weymann', 'Hongqi', 'HSV', 'Triumph', 'DPCA', 'Haima Automobile', 'Ford Motor Company of Canada', 'Moon Motor Car', 'Porsche Automobil Holding SE', 'Société de Véhicules Automobiles de Batilly', 'Bugatti Automobiles', 'Denza', 'Temax', 'Toyota Australia', 'Toyota Motor Manufacturing (UK)', 'Bogdan Group', 'Vehículos Automotores Mexicanos', 'BYD', 'Rover Group', 'Cushman', 'SAIC-GM-Wuling', 'NUMMI', 'S.P.A.', 'ZiL', 'Glas', 'Honda', 'Zastava', 'Nissan', 'BMW', 'Facel', 'Austin Motor Company', 'Renault', 'Peugeot', 'Citroën', 'Aixam', 'Gumpert', 'Armstrong-Whitworth', 'Schweizerische Industrie Gesellschaft', 'Daimler-Motoren-Gesellschaft', 'Geely', 'ChechenAvto', 'AAT', 'Acme', 'Aerocar', 'Ajax', 'Ajax', 'Alter', 'Axon Automotive', 'BMW Brilliance', 'Deere', 'DFL', 'FAW Jilin', 'Ford Performance', 'Franklin', 'General Motors India Private Limited', 'FCA Srbija', 'Holden New Zealand', 'Miura', 'Fiat Group Automobiles', 'Fujian Motors Group', 'Hansa', 'Pyonghwa', 'Volkswagen do Brasil', 'Goliath', 'Ford of Europe', 'Garuda Mataram Motor', 'Hunan Jiangnan Automobile Manufacturing Co., Ltd.', 'Broadspeed', 'NanoFlowcell', 'Tesla Grohmann Automation', 'Abarth', 'Alfa Romeo', 'Alpine', 'Alvis', 'Auto Union', 'Barkas', 'Bitter Automobile', 'Bugatti', 'IKAP', 'Maybach', 'Byton', 'Flanders', 'psa-retail', 'Isuzu Motors India', 'Jetta', 'Clement Talbot Car Factory', 'DeLorean Motor Company', 'BYD Auto', 'Dacia', 'Daimler', 'Datsun', 'Fiat', 'FSC', 'FSO', 'Valmet Automotive', 'Velie', 'NedCar', 'Subaru', 'Talbot', 'Simca', 'Espenlaub', 'Jonway', 'Ascari Cars', 'Zimmer', 'Oldsmobile', 'Zust', 'Spyker', 'Puch', 'Ballot', 'Basse und Selve', 'Brennabor', 'Brabus', 'GM Uzbekistan', 'Eunos', 'Shanghai Maple', 'Ɛ̃fini', 'Iso Rivolta', 'Alta', 'Melkus', 'Berna', 'HQM Sachsenring GmbH', 'Lotec', 'Ancar', 'Renault Samsung Motors', 'Scion', 'Fuldamobil', 'Farman Aviation Works', 'SeAZ', 'Ruf Automobile', 'Saturn Corporation', 'Ford Germany', 'Chery', 'Uri International Vehicle & Equipment Marketing', 'Mercury', 'Changfeng Motor', 'Apal', 'Polski Fiat', 'Aquila Italiana', 'Arab American Vehicles', 'Holland Car', 'DKW', 'Hartge', 'Monteverdi', 'Imperial', 'Diamond T', 'Carlsson', 'Gemballa', 'Sollers JSC', 'Karmann', 'Veritas', 'Artega Automobile', 'PGO', 'Yulon Motor', 'Ashley Laminates', 'Panhard', 'Fabbrica Ligure Automobili Genova', 'Mascot', 'Astra Daihatsu Motor', 'Auburn Automobile', 'Officine Meccaniche', 'Crouch Cars', 'Morris Motors', 'Delahaye', 'Auto 5000', 'Autolatina', 'Automeccanica', 'Automobile Craiova', 'Automobiles L. Rosengart', 'Q793738', 'Baker Motor Vehicle', 'Beijing Benz', 'Bering Motors', 'Nissan Motor Manufacturing UK', 'Caterham Cars', 'Fornasari', 'Wilson-Pilcher', 'Attica', 'Cord Automobile', 'Steinmetz Opel Tuning', 'Charron', 'Brixia-Zust', 'O.S.C.A.', 'Hurtu', 'Ceirano Fabbrica Automobili', 'Ceirano GB & C', 'Chambers Motors', 'Jiangling Motors', 'Chrysler Europe', 'Cisitalia', 'Austin Rover Group', 'Coey', 'FAW Group', 'Plymouth', 'Cooper Motor Corporation', 'Covert', 'Crawford Automobile', 'Derways', 'Q1141638', 'Ford Union', 'Sofasa', 'Morgan Motor Company', 'De Dion-Bouton', 'Delaunay-Belleville', 'Diatto', 'Peel Engineering Company', 'Du Pont Motors', 'Marathon Motors Engineering', 'Elmore', 'Edsel', 'Pars Khodro', 'Nasr', 'Automobiles Lombard', 'Saleen', 'Heuliez', 'Lozier', 'Junior F.J.T.A.', 'Weiertz', 'Bizzarrini', 'Ford-Vairogs', 'Ford Motor Credit Company', 'Ford Performance Vehicles', 'Siata', 'Giad Auto', 'Perodua', 'Winton Motor Carriage Company', 'Standard Motor Company', 'Hyundai Motor India Limited', 'Mitsuoka', 'Hillman', 'Rochet-Schneider', 'TagAZ', 'REO Motor Car Company', 'Rovin', 'LuAZ', 'Hulas Motors', 'Roewe', 'Marcos Engineering', 'Hupmobile', 'Innocenti', 'Q1676117', 'Jordan Motor Car Company', 'Karsan', 'Wallyscar', 'White Motor Company', 'Otosan', 'Micro Cars', 'Anadol', 'Oakland Motor Car Company', 'Somaca', 'Oyak-Renault', 'Lloyd Cars Ltd', 'Markranstädter Automobilfabrik', 'Q1906948', 'Mayer', 'Mercer Automobile Company', 'Q1926325', 'Modiran Vehicle Manufacturing Company', 'Premier Automotive Group', 'Singer Motors', 'Salmson', 'Paige automobile', 'Diamond-Star Motors', 'Rolls-Royce Motors', 'Spartan Cars', 'Petigars Prat Carrabin vehicles', 'Westfield Sportscars', 'Prince Motor Company', 'Pullman automobile', 'Raw Engineering', 'K-R-I-T Motor Car Company', 'S.C.A.P.', 'Automobile Products of India', 'S. Sandford', 'Shinjin Group', 'FAW Tianjin', 'Renault Sport', 'Stearns', 'Stoddard-Dayton', 'Storero', 'Mercedes', 'Temperino', 'Motor Company of Botswana', 'Toyota Motor Manufacturing France', 'Turner Sports Cars', 'General Motors Europe', 'Speedwell Motor Car Company', 'Vencer', 'Zenvo', 'Wyvern Light Car', 'Xinkai', 'Škoda Auto India Private Limited', 'Crossley Motors', 'Laffly', 'Baojun', 'Dorris Motors Corporation', 'Fiat India Automobiles', 'Nakhchivan Automobile Plant', 'AzSamand', 'Unicor Prima Motor', 'Maxus', 'Vigo PSA Factory', 'Avions Voisin', 'Ford India Private Limited', 'PSA Rennes Plant', 'Carrozzeria Viotti', 'Crespi', 'Cosmos Engineering', 'Qoros', 'Autokinitoviomihania Ellados', 'CAMI Automotive', 'Ukrainian Automobile Corporation', 'ABC', 'AZLK', 'Aland', 'Albany', 'Aldo', 'All-Steel', 'Allied', 'American Expedition Vehicles', 'American Honda Motor Company', 'Aptera Motors', 'Ardsley Motor Car Company', 'Arrinera', 'Audi India', 'Austin Automobile Company', 'BMW India', 'Bajaj Group', 'Balzer', 'Beijing Hyundai', 'Brennan Motor Manufacturing Company', 'Buckmobile', 'Bugmobile Company', 'Canadian Electric Vehicles', 'Century Motor Vehicle Company', 'Chase Motor Truck Company', 'Chery Jaguar Land Rover', 'Chevrolet Europe', 'Chevrolet Sales India Private Limited', 'China Motor Corporation', 'Chinkara Motors', 'Climber', 'CAR CLUB', 'Colburn Automobile Company', 'Corbin', 'Cunningham automobile', 'Detroit Auto Vehicle Company', 'Detroit Automobile Company', 'Devon Motorworks', 'Diardi', 'Dolson', 'Dongfeng Liuzhou Motor Company', 'Dongfeng Honda', 'Dragon Automobile Company', 'Eisenhuth Horseless Vehicle Company', 'Elio Motors', 'Oettinger Sportsystems', 'Eterniti Motors', 'Etox', 'FAW Car Company', 'Facansa', 'Factory Five Racing', 'Fenix Automotive', 'Ford Lio Ho Motor', 'Ford Motor Company of New Zealand', 'Ford Motor Company Philippines', 'Ford Tickford Experience', 'Fremont Assembly', 'Frese Motorcars', 'GM Colmotores', 'GM Financial', 'General Motors South Africa', 'Grant', 'Great Southern Automobile Company', 'Grout', 'H. A. Moyer', 'Q5767794', 'W Motors', 'General Motors de Argentina', 'General Motors de México', 'Honda Atlas Cars Pakistan', 'Honda Automobile (China) Company', 'Industria Argentina Vehículos de Avanzada', 'Industrias Eduardo Sal-Lari', 'IDA-Opel', 'Imperial Automobile Company', 'Industrial Development and Renovation Organization of Iran', 'Iroquois Motor Car Company', 'Venirauto', 'Kleemann', 'Litex Motors', 'MG Sports and Racing Europe', 'MK-Motorsport', 'Matheson (auto)', 'Mazda North American Operations', 'Mitsubishi Motors North America', 'Mitsubishi Motors Philippines', 'Moline Automobile Company', 'Monarch', 'Moore Automobile Company', 'Nissan Motor India Private Limited', 'Northern', 'Ohta Jidosha', 'Opel India Private Limited', 'Oscar Lear Automobile Company', 'PPI Automotive Design', 'Państwowe Zakłady Inżynieryjne', 'Pierce-Racine', 'Premier Motor Manufacturing Company', 'Rapid Motor Vehicle Company', 'Renault India Private Limited', 'Renault Nissan Automotive India Private Limited', 'Renntech', 'Royal Motor Company', 'Shanghai GM', 'Sigma Motors', 'Sipani', 'St. Louis Motor Company', 'Stillen', 'Subaru of America', 'Tata Motors Cars', 'Toyota Kirloskar Motor Private Limited', 'Upton', 'Van Wagoner', 'Volkswagen Group Sales India', 'Volkswagen India', 'Walker Motor Car Company', 'Ward', 'Wildfire', 'Woods Motor Vehicle', 'Yale', 'Yema Auto', 'Zagross Khodro', 'Changan Suzuki', 'Fisker Coachbuild', 'Nissan Motor Indonesia', 'Aeon vehicles', 'Q9656340', 'Q10273203', 'Q10302037', 'Q10335617', 'Shineray', 'König Specials', 'General Motors do Brasil', 'NMKV', 'Toyota Motor East Japan', 'Jinbei GM Automotive Company', 'MG Rover Group', 'Dongfeng Yulon', 'Q13422176', 'Ford Romania', 'Hennessey Performance Engineering', 'Fahrzeugbau Ing. Hans Meister', 'Revoz', 'Volkswagen Group Rus', 'Norman Cycles', 'Sarao Motors', 'Honda Cars India', 'LandFighter', 'Q15820970', 'Light Car Company', 'Q15833224', 'Q15834308', 'Replicar', 'Unison', 'Indus Motors Company', 'Landwind', 'Saehan Motors', 'General Motors de Chile', 'Q16612263', 'ZMA', 'Auto Euro Indonesia', 'Drive eO', 'Bell Motor Car Company', 'Mazda Motor Indonesia', 'Green Field Motor', 'Ford Sollers', 'Geronimo Motor Company', 'Harrison', 'Kandi Technologies', 'Mitsubishi Motors Thailand', 'Naza Automotive Manufacturing', 'Toyota Motor Thailand', 'Hyundai Motor America', 'Worthington Automobile Company', 'Caps Brothers Manufacturing Company', 'Bay State Auto Company & R. H. Long Motors Company', 'Kansas City Motor Car Company', 'Ace', 'Avtokam', 'Campagna Corporation', 'Severin Motor Car Company', 'Wonder Motor Car Company', 'Q18477446', 'Rupp Industries', 'Dongfeng Renault', 'Rezvani Automotive Designs', 'Production Automotive Services', 'Driggs-Seabury', 'Hradyesh', 'Q20021613', 'WaterCar', 'Atalanta Motors', 'Innoson Vehicle Manufacturing', 'Land Rover Uzbekistan', 'Q21923394', 'Karma Automotive', 'Corsa Specialised Vehicles', 'Borgward Group AG', 'Minari Engineering', 'Changan Ford Automobile', 'Legacy Classic Trucks', 'Karakoram Motors', 'Fath Vehicle Industries', 'Nimr Automotive', 'Changan PSA', 'Mopetta', 'Firestone-Columbus Automobiles', 'Astro Designs', 'TREKOL', 'car factory', 'Eagle Engineering & Motor Company', 'Moller Motor Company', 'Milan Automotive', 'Hofele-Design', 'Q60850795', 'MG Motor India', 'Dietrich Véhicules', 'Tacoma Motor Corporation', 'Stellantis', 'Audi', 'AC Cars', 'Austro-Daimler', 'Autobianchi', 'Borgward', 'Brasier', 'Bristol Cars', 'Buick', 'Daewoo Motors', 'Daimler Company', 'Delage', 'Dodge', 'Infiniti', 'Itala', 'Jensen Motors', 'Lada', 'Laurin & Klement', 'Mathis', 'Matra', 'Oltcit', 'Pierce-Arrow', 'Pontiac', 'TVR', 'Hispano-Suiza', 'Holden', 'Horch', 'Chevrolet', 'Skoda', 'Jaguar', 'Kia', 'Koenigsegg', 'Lancia', 'Lotus Cars', 'MG Car Company Limited', 'Mitsubishi Motors', 'NSU', 'Opel', 'Hyeondae', 'Motorlet', 'Hyundai Motor Group', 'Packard', 'Porsche', 'Saab', 'Toyota']
reviewProduct='hodinky'
brands=brandFinder.findBrands(reviewProduct)
#brands=[]
product=brandFinder.findProductNames(reviewProduct)
product=[x.lower() for x in product]
print(product)
print(brands)
resultDict=dict()
reviewUrls=list()
SpecialProduct=False
if(reviewProduct=='kniha'):
	reviewUrls=['idnes','iliteratura']
	SpecialProduct=True
elif(reviewProduct=='film'):
	reviewUrls=['lidovky','idnes','novinky']
	SpecialProduct=True



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


def readReviews(link):
	reviewWordsListPart = ['recenze','hodnoceni','test']

	datafile=open(link,"r",encoding="utf8")

	dataContent=datafile.read()
	dataContentList=dataContent.split('<doc')
	cnt=0
	

	BrandWeight=0.5
	ProductWeight=10
	ReviewWeight=0


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
		paragraph=''
		ArticleProduct=''
		ArticleHead=''
		ParagraphTagsS=0
		ParHeading=False
		ArticleHeadFlag=False
		for line in x.splitlines():


			if(firstLine==True):

				firstLine=False
				url=line.split('url="')[-1].split('"')[0]
				if('comment' in url.split('#')[-1] or '.sk' in url or 'tipcars' in url):
					break
				urlName=url.split('.')[1]
				if('www' in url.split('.')[0] ):
					urlName=url.split('.')[1]
				else:
					urlName=url.split('.')[0].split('/')[-1]
				
				if(urlName not in reviewUrls and len(reviewUrls)!=0):
					break

				IsReview=0
				IsProduct=0
				IsBrand=0
			#if(line.startswith('<p')):
			
			ParagraphLines.append(line)
			if(line.startswith('<head')):
				ArticleHeadFlag=True
			if(line.startswith('<link')):
				LinkInPar=True
			if(line.startswith('<s>')):
				ParagraphTagsS+=1
			if(line.startswith('<h')):
				ParHeading=True
			if(line.startswith('</p')):
				#if(not LinkInPar):
				#if(ParagraphTagsS>2 or ArticleHeadFlag): #or (ParHeading and not LinkInPar)):
				if((ParagraphTagsS>2 or ArticleHeadFlag)): #or (ParHeading and not LinkInPar)):
					#paragraph=list()
					
					if(ArticleHeadFlag):

						BrandWeight=10
						ProductWeight=20
						#ReviewWeight=30
						ReviewWeight=30
				
					else:

						BrandWeight=0.5
						ProductWeight=10
						ReviewWeight=0
					

					for ParagraphLine in ParagraphLines:
						if(not ParagraphLine.startswith('<')):
							lineList=ParagraphLine.split('\t')							
							#paragraph.append(lineList[1])
							if('title' not in ParagraphLine):
								if(ArticleHeadFlag):
									ArticleHead+=lineList[1]+' '
								else:
									paragraph+=lineList[1]+' '
							if('NN' in lineList[2]):
								ParagraphLine=lineList[3]
								#print(ParagraphLine)
								#paragraph.append(ParagraphLine)
								#print(ParagraphLine)

								
								#if(SubstrInList(ParagraphLine,reviewWordsListPart)):
								if(ParagraphLine.lower() in reviewWordsListPart):
									#print(ParagraphLine)
									WordResult+=ReviewWeight
									IsReview+=1
									#print('\t\t\t\t\t\t',ParagraphLine)
								
								#if(SubstrInList(ParagraphLine,brands)):
								if(ParagraphLine in brands):
									#print('WOR: ',ParagraphLine)
									WordResult+=BrandWeight
									IsBrand+=1
									#print(ParagraphLine)
								


								#if(SubstrInList(ParagraphLine,product)):
								if(ParagraphLine.lower() in product):
									#print('WOR: ',ParagraphLine)
									WordResult+=ProductWeight
									IsProduct+=1

								#print(ParagraphLine)
					#print(' '.join(paragraph),'.')
				LinkInPar=False
				ParagraphLines=list()
				ParagraphTagsS=0
				ParHeading=False
				ArticleHeadFlag=False


		Result=UrlResult*1+WordResult
		'''
		if(IsReview>0):
			if(IsProduct+IsBrand>0):
				#if(IsBrand+IsProduct*2>20):

				#	print('\n\t\t\t',url,': ',end='')
				#else:
				print('\n',url,': ',end='')
				print('Review: ',IsReview,end=' ')
				print('Product: ',IsProduct,end=' ')
				print('Brand: ',IsBrand,end=' ')
				print('P+B: ',IsBrand+IsProduct,end=' ')
				#resultDict[url]=[IsBrand*BrandWeight+IsProduct*ProductWeight+IsReview*ReviewWeight , IsBrand, IsProduct, IsReview]
				resultDict[url]=[WordResult , IsBrand, IsProduct, IsReview]
				print('\n\t\t','Nadpis:',ArticleHead,'\n')
				print('\n\t\t',paragraph,'\n')
		else:
			if(IsProduct+IsBrand>0):
				print('\n\t\tMaybe review:',url,end=' ')
				#print('Review: ',IsReview,end=' ')
				print('Product: ',IsProduct,end=' ')
				print('Brand: ',IsBrand,end=' ')
				print('P+B: ',IsBrand+IsProduct,end=' ')
				resultDict[url]=[WordResult , IsBrand, IsProduct, IsReview]
				print('\n\t\t',paragraph,'\n')
		'''
		if(WordResult>0 and IsProduct>0 and IsReview>0):
		#if(WordResult>0 and IsProduct>0):
			urlName=url.split('.')[1]
			if('www' in url.split('.')[0] ):
				urlName=url.split('.')[1]
			else:
				urlName=url.split('.')[0].split('/')[-1]

			if(not SpecialProduct):
				for headPart in ArticleHead.split(' '):
					if(len(headPart)>0):
						if(headPart[0].isupper() or headPart.isdigit()):
							if(headPart.lower() in url and headPart.lower() not in reviewWordsListPart):
								if(headPart.lower() not in urlName):
									ArticleProduct+=headPart+' '
			
				if(reviewProduct=='auto'):
					if(not ProductFinder.WebScrape_productAuto(ArticleProduct)):				
						continue
				else:
					#if(False):
					if(not ProductFinder.WebScrape_product(ArticleProduct)):
						continue

			else:
				if(reviewProduct=='kniha'):

					try:
						uClient = uReq(url)
					except:
						continue

					page_html = uClient.read()
					#print(page_html)
					uClient.close()
					page_soup = soup(page_html, "html.parser")
					if(urlName=='idnes'):
						try:
							ArticleProduct=page_soup.findAll("h3",{"itemprop":"name"})[0].text
						except:
							continue
					elif(urlName=='iliteratura'):
						try:
							OriginalHead=page_soup.findAll("h1",{"itemprop":"name headline"})[0]
							OriginalHead.select("br")[0].replace_with("\n")
							ArticleProduct=OriginalHead.text.split('\n')[-1].strip()
						except:
							continue
				elif(reviewProduct=='film'):
					try:
						uClient = uReq(url)
					except:
						continue

					page_html = uClient.read()
					#print(page_html)
					uClient.close()
					page_soup = soup(page_html, "html.parser")
					if(urlName=='idnes'):
						try:
							ArticleProduct=page_soup.findAll("h3",{"itemprop":"name"})[0].text
						except:
							continue
					elif(urlName=='lidovky'):
						try:
							ArticleProduct=page_soup.find("table",{"class","complete not4bbtext"}).find('span').text
						except:
							continue
					elif(urlName=='novinky'):
						try:
							ArticleProduct=page_soup.findAll("div",{"class":"infobox"}).text
						except:
							continue

			print('\n\t\treview:',url,end=' ')
			print('Review: ',IsReview,end=' ')
			print('Product: ',IsProduct,end=' ')
			print('Brand: ',IsBrand,end=' ')
			print('P+B: ',IsBrand+IsProduct,end=' ')

			resultDict[url]=[WordResult , IsBrand, IsProduct, IsReview,ArticleProduct.strip(),urlName]

			print('\n\t\t','Nadpis:',ArticleHead,'\n')
			print('\n\t\t','product:',ArticleProduct,'\n')
			print('\n\t\t',paragraph,'\n')
			#if(ProductFinder.WebScrape_product(ArticleProduct)):
			if(False):

				print('\n\t\treview:',url,end=' ')
				print('Review: ',IsReview,end=' ')
				print('Product: ',IsProduct,end=' ')
				print('Brand: ',IsBrand,end=' ')
				print('P+B: ',IsBrand+IsProduct,end=' ')

				resultDict[url]=[WordResult , IsBrand, IsProduct, IsReview,ArticleProduct,urlName]

				print('\n\t\t','Nadpis:',ArticleHead,'\n')
				print('\n\t\t','product:',ArticleProduct,'\n')
				print('\n\t\t',paragraph,'\n')

			'''
			for x in ArticleHead.split(' '):
				if(x.lower() in url and x.lower() not in reviewWordsListPart):
					ArticleProduct+=x+' '
			'''

	#print(sorted(resultDict.items(), key=lambda j: j[1]))
			#if(IsBrand>0):
				#print('Brand: ',IsBrand,end=' ')
for x in os.listdir('..\Data\parsed\\'):
	#FindReviews('..\Data\\'+x)
	readReviews('..\Data\parsed\\'+x)
'''
readReviews('..\Data\parsed\\2020-09-11.parsed')
'''
	


sortedDictlist=sorted(resultDict.items(), key=lambda j: j[1])
for x in sortedDictlist:
	#pass
	print(x)
