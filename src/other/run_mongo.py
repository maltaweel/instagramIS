'''
Created on Jan 5, 2018

@author: TDBP1

Module to use MongoDB

'''

from pymongo import MongoClient
import pymongo
from bson.binary import Binary
import sys
import re
from datetime import date

class mongo: 
    
    '''
    @param collectionName: the geotag code inputted by user
    collectionName is used to name/identify a collection
    '''
    def __init__(self,collectionName):
        self.collectionName=collectionName
    
    '''
    Start the client using MongoDB
    '''
    def getdatabase(self):
        client=MongoClient('localhost',27017)
        db=client.test_database
        
        return db
    
    '''
    Clear any data pre-existing in the collection
    '''
    def clearDB(self):
        client=MongoClient('localhost',27017)
        db=self.getdatabase()
        
        #create collection name. MongoDB collections must being with a letter or underscore
        col='c'+self.collectionName
        db.drop_collection(col)
        
    '''
    Populate the insta collection
    @param i: the ID number
    @param jpgLink: .jpg link to the photo image
    @param caption: the caption of the Instagram post
    @param date: the date of post
    '''
    def runinstamongo(self,i,jpgLink,caption,date):
        self.i=i
        self.jpgLink=jpgLink
        self.captionUni=caption
        self.date=date
        
        #get the database
        db=self.getdatabase()
        
        #create the collection
        col='c'+self.collectionName
        
        insta=db[col]
        
        
        post = {'ID': i,
              'JPG Link': jpgLink,
              'Caption': caption,
              'Date': date
              }
        
        #post to collection
        post_id = insta.insert_one(post).inserted_id
        post_id
        
        
        
        
