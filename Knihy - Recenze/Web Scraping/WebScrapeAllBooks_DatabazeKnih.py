import sys
import WebCrawl_DatabazeKnih_vsechnyKnihy

# parallel-ssh -i -t 0 -A -h Hosts2 python3 /mnt/minerva1/nlp/projects/sentiment9/Scripts/WebScrapeAllBooks_DatabazeKnih.py  \$HOSTNAME

#celkovy pocet stranek v databazi knih
maxCount = 4592


PCcount = 5 #pocet zarizeni na kterych skript pobezi

arg=sys.argv[1]

Divcount = round((maxCount/PCcount)+0.4)
for x in range (1,PCcount+1):

	try:
	    val = int(arg[-1:])
	except ValueError:
		val = 1


	if(x == val):
		WebCrawl_DatabazeKnih_vsechnyKnihy.FindBookUrls((Divcount*(x-1))+1,Divcount*x)
