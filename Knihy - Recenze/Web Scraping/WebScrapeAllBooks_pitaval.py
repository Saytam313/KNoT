import sys
import WebCrawl_pitaval_vsechnyKnihy
# parallel-ssh -i -t 0 -A -h Hosts python3 /mnt/minerva1/nlp/projects/sentiment9/Scripts/WebScrapeAllBooks_cbdb.py  \$HOSTNAME

arg=sys.argv[1]

x=arg[-2:]
WebCrawl_pitaval_vsechnyKnihy.FindBookUrls(x)
