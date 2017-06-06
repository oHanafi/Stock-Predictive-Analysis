
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
import goslate 
                
gs = goslate.Goslate()
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
                
                
        
                if link: # Check if link is not empty
                        
                        html = urllib.urlopen(link).read()
                        Title = ""
                        Author = ""
                        soup2 = BeautifulSoup(html, "html.parser")
                        news = []
  

                        news = soup2.findAll('p', {"class" : "lead"}) + soup2.findAll('img', {"class" : "alignRight"})
                        
                        # The article has to be placed in the database for version 0.2.
                        print ("\n")
                        print ("=====================================================")
                        print ("\n")
                        #print PolaritySum/80
                        lijstje = []

                        news = list(soup2.findAll('div', {"class" : "reactieContent"}))
                        for com in news:
                                com = str(com)[int(str(com).find('\n\t\t\t\t\t')):]
                                #com = com[:int(str(link).find('\n\t\t\t\t\t\n\t\t\t\t'))]
                                com = com.replace("\n\t\t\t\t\t\n\t\t\t\t</div>", " ")
                                com = " ".join(com.split())
                                #print com
                        lijstje2 = []
                        print(gs.detect("jij bent mooi"))
                        sys.exit()

                        for com in lijstje:
                                    
                                print ("\n")
                                print ("=====================================================")
                                print ("\n")
                                #x = x + 1
                                    
                                print(type(com))
                                PolaritySum = TextBlob(com).sentiment.polarity
                                Subjectivity = TextBlob(com).sentiment.subjectivity
                                lijstje.append(com)
                                translate = gs.translate(com, 'en')
                                print(com)
                                print (gs.detect(com))

                                    
                        for j in lijstje:
                                j = gs.translate(j, 'nl')

                                lijstje2.append(j)

                        #print lijstje2
                                


                        

                        sys.exit()

                        with open('Stats.csv', 'w') as csvfile:
                            fieldnames = ['Comment', 'Polarity', 'Subjectivity']
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            x = 0
                            for com in lijstje:
                                    
                                    print ("\n")
                                    print ("=====================================================")
                                    print ("\n")
                                    x = x + 1
                                    
                                
                                    PolaritySum =TextBlob('Stupid').sentiment.polarity
                                    Subjectivity = TextBlob(str(com)).sentiment
                                    print com
                                    print PolaritySum
                                    print Subjectivity
                                    writer.writerow({'Comment': x, 'Polarity': PolaritySum, 'Subjectivity' : Subjectivity})

                            
                            

                        
                        
                        

x = -10
while x < 0:
    pullNews()
        

    
    
