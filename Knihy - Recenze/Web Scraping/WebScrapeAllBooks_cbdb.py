import sys
import WebCrawl_cbdb_vsechnyKnihy
# parallel-ssh -i -t 0 -A -h Hosts python3 /mnt/minerva1/nlp/projects/sentiment9/Scripts/WebScrapeAllBooks_cbdb.py  \$HOSTNAME

maxCount = 2231 #celkovy pocet stranek v databazi knih

PCcount = 38 #pocet zarizeni na kterych skript pobezi

arg=sys.argv[1]

Divcount = round((maxCount/PCcount)+0.4)
for x in range (1,PCcount+1):
	if(x == int(arg[-2:])):
		WebCrawl_cbdb_vsechnyKnihy.FindBookUrls((Divcount*(x-1))+1,Divcount*x)
