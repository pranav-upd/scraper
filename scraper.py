import re
from bs4 import BeautifulSoup
import mechanicalsoup
import csv

def totext(html):
    reg_compile = re.compile('<.*?>')
    totext1 = re.sub(reg_compile, '', html)
    totextn = re.sub('\n', '', totext1)
    reg_compile2 = re.compile(r'\s+\B\s+')
    totext2 = re.sub(reg_compile2, ',', totextn)
    totext3 = re.sub(' ', '-', totext2)
    totext4 = re.sub(',', ' ', totext3)
    return totext4

browser = mechanicalsoup.Browser()
data1 = browser.get("https://books.toscrape.com/index.html")
p1 = data1.soup.find_all('div',{'class':'side_categories'})
#-------------------------------------------------
#       Variables and lists
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
bname = ""
bcost = ""
bstock_status = ""
l1_index= 2
#---------------------------------------------------
#............
#............
for x in p1:
    x = totext(str(x))
    list1.append(x.split())
for f in list1:
    list6.extend(f)
list6.remove("Books")    
#..........................................
#..........................................
for d in list6:
    d = d.lower()
    data2 = browser.get(f'https://books.toscrape.com/catalogue/category/books/{d}_{l1_index}/index.html')
    print(f'https://books.toscrape.com/catalogue/category/books/{d}_{l1_index}/index.html {data2}')
    p2 = data2.soup.find_all('article',{'class':'product_pod'})
#................
#................
    for a in p2:
        for z in a:
            z = totext(str(z))
            list2.append(z.strip().split())
        for b in list2:
            for c in b:
                list3.append(c)        
        bname = list3[0]
        bcost = list3[1]
        bstock_status = list3[2]
            
        with open('scraper_data.csv','a') as myfile:
            sd = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL)
            sd.writerow([bname, bcost, bstock_status])   
        list2.clear()
        list3.clear()
    l1_index = l1_index+1
print("Done :)")    

#.......
#.......
    



    
    
    
    
        


