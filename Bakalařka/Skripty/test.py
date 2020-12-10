urlList=['test','noveho','bugattka','veyron']
brandList=['Škoda Auto','Automobiles Ettore Bugatti','Ford']

for x in urlList:
    for y in brandList:
        if(x.lower() in y.lower()):
            print(x)

print('skoda' == 'škoda')