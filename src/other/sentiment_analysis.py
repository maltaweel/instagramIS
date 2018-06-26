'''
Created on Jan 2, 2018

@author: TDBP1

Module to get data from MongoDB and perform sentiment intensity analysis.

'''

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
import os
import unicodecsv as csv
import re
from run_mongo import mongo

class SentimentAnalysis:
    pass

    '''
    @param db: MongoDB database
    Create path to CSV file
    '''
    def __init__(self,db,collectionName):
        self.db=db
        self.collectionName=collectionName
        
        #create path to output file
        pn=os.path.abspath(__file__)
        pn=pn.split('src')[0]
        path=os.path.join(pn,'output')
        
        filename=path+'/'+'sentiment_intensity_results.csv'
        
        self.csvfile=filename
    
    '''
    Method to convert captions from strings to 
    tokenized list/text
    
    @return captionTextList: list of captions, where words have been tokenized
    @return captionFullText: one string of concatenated captions, where words have been tokenized
    '''
    def getCaptions(self):
        
        db=self.db

        captionTextList=[]
        captionFullText=''
        
        #get a list of all distinct IDs
        #all IDs are distinct so this number will equal the number of posts scraped
        IDs=db.insta.distinct('ID')
        
        for ID in IDs:
            
            col='c'+self.collectionName
            
            #find the document for each ID
            cursor=db[col].find({'ID': ID})
            
            for document in cursor:
                
                #create a empty string variable to which tokenized words will be concatenated
                captionText=''
                
                #get the caption from the 'Caption' field
                caption=document['Caption']
                
                #tokenize the caption
                tokens = word_tokenize(caption)
                
                for token in tokens:
                    
                    #contatenate 
                    captionText=captionText+' '+token
                    captionFullText=captionFullText+' '+token
                #append the concatenated string to the captionTextList.
                captionTextList.append(captionText)
            
        return captionTextList,captionFullText
    
    '''
    Method to measure sentiment intensity.
    Uses nltk.sentiment.vader library.
    Writes data into csv file.
    
    @param captions: a list of captions
    '''           
    def sentimentIntensity(self,captions):
                
        sid = SentimentIntensityAnalyzer()
        
        #create field names on CSV
        fieldnames = ['Caption','Compound','Negative','Neutral','Positive']
        
        with open(self.csvfile, 'wb') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()

            for caption in captions:
                
                if caption==u'':
                    continue
                
                #get polarity scores
                ss = sid.polarity_scores(caption)
                com=()
                neg=()
                neu=()
                pos=()
                
                for k in sorted(ss):
                    
                    #find the polarity score values 
                    if str(k)=='compound': 
                        com=ss[k]
                    if str(k)=='neg':    
                        neg=ss[k]
                    if k=='neu':
                        neu=ss[k]
                    if k=='pos':
                        pos=ss[k]
                
                #write the scores into CSV                    
                writer.writerow({'Caption': caption,
                                 'Compound': com,
                                 'Negative': neg,
                                 'Neutral': neu,
                                 'Positive': pos
                                    })
 