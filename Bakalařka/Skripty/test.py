

datafile=open('..\Data\parsed\\2019-01-25_0215.parsed',"r",encoding="utf8")

dataContent=datafile.read

cnt=0
debug=0
for x in dataContent.split('<doc'):
    print(x)


    if(debug==1):
        for line in x.splitlines():
            if(line[0].isnumeric()):
                lineList=line.split('\t')
                if('NN' in lineList[2]):
                    print(lineList[1])
                #print(line.split('\t'))
    if(cnt>0):
        break
    cnt+=1

