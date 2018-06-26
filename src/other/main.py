'''
Created on Jan 5, 2018

@author: TDBP1

Main module for this program.
The module calls on four other modules (below)
1) run_mongo 
2) instagram_script
3) sentiument_analysis
4) frequency_dist

Webscrapes an Instagram geotag.
Outputs a CSV file for sentiment intensity analysis
and a CSV file for word frequency distribution based on scraped captions.
'''

from instagram_script import InstaScraper
from sentiment_analysis import SentimentAnalysis
from run_mongo import mongo
from frequency_dist import WordFrequency
import time

#get user input
while True:
    try: 
        #get input from user
        code=int(input('What is the instagram location code? \n For example, enter 354060703 if the geotag url is \n https://www.instagram.com/explore/locations/354060703/trafalgar-square/ \n'))
    
    except NameError:
        print ('Please enter a string of numbers')
    except ValueError:
        print ('Please enter a string of numbers')   
    except SyntaxError:
        print ('Please enter a string of numbers')       
    else:
        break

while True: 
    try:         
        numberInsta=int(input('How many instagrams would you like to analyze? \n'))
    except NameError:
        print ('Please enter a string of numbers')
    except ValueError:
        print ('Please enter a string of numbers')   
    except SyntaxError:
        print ('Please enter a string of numbers')       
    else:
        break


ls = [str(code)]
numberInsta=numberInsta+9

#call on mongo class with the geotag code (which is used to name Mongo collection)
m=mongo(ls[0])

#clear previous data in MongoDB the collection
m.clearDB()

#run instagram scraping
s=InstaScraper("/Users/Ed/eclipse/chromedriver",ls,numberInsta)
s.runScraper()
print('Scraping Complete')

#connect to database with webscraped data
db=m.getdatabase()

#run sentiment analysis
c=SentimentAnalysis(db,ls[0])
captions,captionText=c.getCaptions()
c.sentimentIntensity(captions)

#run frequency distribution analysis
freq=WordFrequency(captionText)
freq.getFreqDist()

print('Analysis Complete')




