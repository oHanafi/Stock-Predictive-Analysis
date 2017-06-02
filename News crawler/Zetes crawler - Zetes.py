import requests
import json
import urllib
from bs4 import BeautifulSoup
from textblob import TextBlob
import feedparser
import pytest
import pyodbc
import sys
import re
import csv
  

def pullNews():

   
        url = "https://www.tweakers.net/zoeken/?keyword=zetes"
        html = urllib.urlopen(url).read()
        soup = BeautifulSoup(html, "html.parser")
            
        listNews = soup.findAll('p', {"class" : "title ellipsis"})
            
        Writer = "Tweakers"

        PolaritySum = 0

        for link in listNews:
                link = str(link)[int(str(link).find('href'))+6:]
                link = str(link)[:int(str(link).find('">'))]
                print link
                
        
                if link: # Check if link is not empty
                        print(link)
                        html = urllib.urlopen(link).read()
                        Title = ""
                        Author = ""
                        soup2 = BeautifulSoup(html, "html.parser")
                        news = []
  

                        news = soup2.findAll('p', {"class" : "lead"}) + soup2.findAll('img', {"class" : "alignRight"})
                        
                        print news
                        sys.exit("lol")

                        Content = ""
                        for paragraph_tag in soup2.find_all('p'):
                        #print paragraph_tag.text
                                Content = Content + paragraph_tag.text

                        print Content
                        #print(Content)
                        #addToNews(Title, Content, Author , link, '2014/12/20 10:12:30')
                        AnalyseThis = TextBlob(Content)
                        print ("Sentiment: " + str(AnalyseThis.sentiment.polarity))
                        PolaritySum = PolaritySum + AnalyseThis.sentiment.polarity

                        # The article has to be placed in the database for version 0.2.
                        print ("\n")
                        print ("=====================================================")
                        print ("\n")
                        print PolaritySum/80

x = -10
while x < 0:
    pullNews()
        

    print ("10 minute break \n")
    time.sleep(600)
    
