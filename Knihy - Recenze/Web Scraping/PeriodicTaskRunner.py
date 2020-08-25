import time


minCnt=0
while True:
	time.sleep(10) #cekani 10min
	exec(open("./cbdbAktualizace.py").read())
	if(minCnt%3==0):#spusteni kazdych 30min
		exec(open("./DatabazeKnihAktualizace.py").read())


	if(minCnt>=7):#spusteni kazdych 24h
		exec(open("./DatabazeKnihReadNewReviews.py").read())
		exec(open("./cbdbReadNewReviews.py").read())
		minCnt=0
  	
	minCnt+=1
