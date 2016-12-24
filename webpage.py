import requests
from bs4 import BeautifulSoup
import csv

web = {}
for n in range(0, 20):
    url = 'http://www.alexa.com/topsites/countries;'+str(n)+'/NZ'
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "lxml")
    nums = soup.find_all("div", {"class": "count"})
    pages = soup.find_all("p",{"class":"desc-paragraph"})

    numgroup=[]
    for num in nums:
        numgroup.append(num.text)

    pagegroup=[]
    for page in pages:
        pagegroup.append(page.text)

    for x in range(len(numgroup)):
        data = {numgroup[x]:pagegroup[x]}
        web.update(data)

    print "finished page " + str(n)
print web

with open('mycsvfile.csv','wb') as f:
    w = csv.writer(f)
    w.writerows(web.items())
    f.close()
