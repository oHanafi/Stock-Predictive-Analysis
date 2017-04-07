import requests
import json
import urllib
from bs4 import BeautifulSoup
from textblob import TextBlob

x=0
url = "https://news.google.com/news?pz=1&hl=en&tab=nn"
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)
linklist = []
#link = "http://www.bbc.com/news"
for link in soup.find_all('a'):
   link.get('href')
   #linklist.append(link.get('href'))

searchCrit = 'Donald'

for x in linklist:
    if searchCrit in x:
        print x
  

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


