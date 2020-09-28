import sys
import WebCrawl_legie_vsechnyKnihy
# parallel-ssh -i -t 0 -A -h Hosts3 python3 /mnt/minerva1/nlp/projects/sentiment9/Scripts/WebScrapeAllBooks_legie.py  \$HOSTNAME

arg=sys.argv[1]

x=int(arg[-2:])
WebCrawl_legie_vsechnyKnihy.FindBookUrls(x)
