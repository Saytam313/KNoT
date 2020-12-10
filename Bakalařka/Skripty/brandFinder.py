from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import requests

#vyhleda firmy ktere maji zadany produkt ve svých výrobcích
def findBrands(product):
    API_ENDPOINT = "https://www.wikidata.org/w/api.php"

    query = product
    #vyhledani id zadaneho produktu
    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'cs',
        'search': query
    }

    r = requests.get(API_ENDPOINT, params = params)

    WikidataID=r.json()['search'][0]['id']

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    #vyhledani kde je produkt zminen v sekci 'Products and Materials' na wikidatech
    sparql.setQuery("""
    SELECT ?item ?itemLabel (GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list)
    WHERE {
      ?item wdt:P1056 wd:"""+WikidataID+""" .
      OPTIONAL { ?item skos:altLabel ?altLabel . FILTER (lang(?altLabel) = "en") }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en" .}
    }
    GROUP BY ?item ?itemLabel
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    brandList=list() 

    #print(results["results"]["bindings"][0]["altLabel_list"]["value"].split(','))

    '''
    for x in results["results"]["bindings"]:
        for y in x["itemLabel"]["value"].split(' '):
            brandList.append(y)
    '''
    AltFoundFlag=False
    for x in results["results"]["bindings"]:
        if(len(x["itemLabel"]["value"].split(' '))>1):
            for y in x["altLabel_list"]["value"].split(','):
                if(len(y.split(' '))==1):
                    if(len(y)<2):
                        continue
                    brandList.append(y)
                    AltFoundFlag=True
                    break
            if(not AltFoundFlag):
                brandList.append(x["itemLabel"]["value"])
            AltFoundFlag=False
        else:
            brandList.append(x["itemLabel"]["value"])

    #brandList=filterBrands(brandList)
    #print(brandList)
    return brandList

#overi ktere ze zadaneho seznamu slov jsou nazvy firem 
def filterBrands(brandList):
    CorrectBrands=list()
    for x in brandList:
        API_ENDPOINT = "https://www.wikidata.org/w/api.php"

        query = x
        #vyhledani id zadaneho produktu
        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': query
        }

        r = requests.get(API_ENDPOINT, params = params)
        SearchResultCounter=1
        GoodResult=False
        for SearchResult in r.json()['search']: #kontrola prvních 2 vysledku hledani podle nazvu jestli se nejedna o firmu
            if(SearchResultCounter >=2):
                break
            else:
                SearchResultCounter+=1
            WikidataID=SearchResult['id']
            params = {
                'action': 'wbgetentities',
                'format': 'json',
                'ids': WikidataID
            }
            r = requests.get(API_ENDPOINT, params = params)
            CompanyWordIDs=['Q4830453','Q6881511','Q786820','Q42855995','Q15081030']
            #Q4830453 - business
            #Q6881511 - enterprise
            #Q786820 - automobile manufacturer
            #Q42855995 - motorcycle manufacturer
            #Q15081030 - manufacturing company


            #nehledat podle konkretniho statementu ale jestli je tam ta kategorie
            #zkusit vyhledat alt nazvy ktery jsou jen o delce jednoho, nebo nějak zkusit udělat že ikdyž to bude vice slovnej název tak se to bude rovnat možna nějakou funkci na to nebo tak

            if('P1056' in r.json()['entities'][WikidataID]['claims'].keys()):
                print("Good: ",query)
                CorrectBrands.append(query)
                GoodResult=True
                break
            else:
                print("Bad: ",query)
            '''
                print(r.json()['entities'][WikidataID]['claims']['P31'])
                for x in r.json()['entities'][WikidataID]['claims']['P31']:
                    
                    if(x['mainsnak']['datavalue']['value']['id'] in CompanyWordIDs):
                        print('Good:',query)
                        CorrectBrands.append(query)
                        GoodResult=True
                        break
                    else:
                        print('Bad:',query)
            '''
            if(GoodResult):
                GoodResult=False
                break
        #print(r.json()['entities'][WikidataID]['claims']['P31'])
        #break
    return(CorrectBrands)
        #WikidataID=r.json()['search'][0]['id']

#print(findBrands('auto'))
#filterBrands(['Samsung'])
