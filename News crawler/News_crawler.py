import requests
import json
import urllib
from bs4 import BeautifulSoup
from textblob import TextBlob
import feedparser
import pytest
import pyodbc

def ophalen(link):
    feed = feedparser.parse(link)
    linklist = []
    for entry in feed.entries:
           if entry["description"].find("AMD") >= 0:
            #assert "AMD" in entry
            print entry["link"]
            print entry["description"]
            print "\n"
            linklist.append(entry["link"])
           else:
              continue
    return linklist



python = "http://www.marketwatch.com/investing/stock/amd/news"
print ophalen(link = python)

htmllink = []

##for url in ophalen(python):
##   html = urllib.urlopen(url).read()
##   soup = BeautifulSoup(html, "html.parser")
##   print soup.findAll('div', {"class" : "Cf"})

x=0
url = python
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
linklist = []
#link = "http://www.bbc.com/news"
lijstje = soup.findAll('li', {"class" : "fnewsitem"})

##a[start:end] # items start through end-1
##a[start:]    # items start through the rest of the array
##a[:end]      # items from the beginning through end-1
##a[:]         # a copy of the whole array

for links in lijstje:
    link = str(links)[int(str(links).find('/story')):]
    link = link[:int(str(link).find('"'))]
    if link:
        print("www.marketwatch.com" + link)
    #checken of in database staat en dan pas opslaan + analyse




##for a in lijstje:
##    print a

print len(lijstje)
   #print a
   #print b
   #print c
   #print "\n"
  

# kill all script and style elements
for script in soup(["script", "style"]):
   script.extract()    # rip it out



# get text
text = soup.get_text()


# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)



wiki = TextBlob(text)
r = wiki.sentiment.polarity
t = wiki.sentiment.subjectivity


#To-Do:
#1. Filter websites adhv variabele en ga naar deze websites.
#2. Haal alleen artikelen op en dus niet alle rotzooi eromheen.
#3. Sla deze in een list op per url.
#4. Analyseer deze op nog te kiezen perspectieven.
#5. Adhv resultaten analyses pas imago/status bedrijf aan.



