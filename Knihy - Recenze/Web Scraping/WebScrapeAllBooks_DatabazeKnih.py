import sys
import WebCrawl_DatabazeKnih_vsechnyKnihy
# parallel-ssh -i -A -h Hosts python3 /mnt/minerva1/nlp/projects/sentiment9/Scripts/test.py  \$HOSTNAME

maxCount = 4510 #celkovy pocet stranek v databazi knih

PCcount = 30 #pocet zarizeni na kterych skript pobezi

arg=sys.argv[1]

Divcount = round((maxCount/PCcount)+0.5)
for x in range (1,PCcount+1):
	if(x == int(arg[-2:])):
		WebCrawl_DatabazeKnih_vsechnyKnihy.FindBookUrls((Divcount*(x-1))+1,Divcount*x)
