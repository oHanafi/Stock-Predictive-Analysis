import requests
import json
import urllib
from bs4 import BeautifulSoup
from textblob import TextBlob

url = "https://news.google.com/news?pz=1&hl=en&tab=nn"
html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)
linklist = []
#link = "http://www.bbc.com/news"
for link in soup.find_all('a'):
   linklist.append(link.get('href'))

for l in linklist:
   if ('Russia' in l):
        print l
    
    
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

print r
print t


