'''
Created on Jan 5, 2018

@author: TDBP1

Module to analyze word frequency.
'''

from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk
from nltk.corpus import stopwords
from cgitb import text
import os
import unicodecsv as csv

class WordFrequency():
    pass

    '''
    @param text: all captions in one string value
    Create path to CSV file
    '''
    def __init__(self,text):
        self.text=text
    
        pn=os.path.abspath(__file__)
        pn=pn.split('src')[0]
        path=os.path.join(pn,'output')
        
        filename=path+'/'+'freqdist_results.csv'
        
        self.csvfile=filename
    
    
    '''
    Method to get word frequency outcome analysis.
    Outputs CSV file
    '''
    def getFreqDist(self):
        
        fieldnames = ['Word','Frequency']
        
        with open(self.csvfile, 'wb') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            text=self.text
        
            #set stopwords
            stopwords = set(nltk.corpus.stopwords.words('english'))
                   
            words=word_tokenize(text)
            
            #remove words if length of word is not over 1 (i.e. punctuation)
            words = [word for word in words if len(word) > 1]
            #remove numbers
            words = [word for word in words if not word.isnumeric()]
            #make all words lowercase
            words = [word.lower() for word in words]
            #remove stopwords
            words = [word for word in words if word not in stopwords]
                
            fdist= FreqDist(words)

            #number of all words
            print ('Total number of samples: %i' % fdist.N())
            
            #number of all distinct words
            print ('Total number of bins: %i' % fdist.B())
            
            #write all bins and count into CSV file
            for word, frequency in fdist.most_common(fdist.B()):
                writer.writerow({'Word':word,'Frequency': frequency})
            
        