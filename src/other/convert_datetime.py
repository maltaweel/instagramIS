'''
Created on Dec 26, 2017

@author: TDBP1

Module to convert date and time string 
into date format.

'''
from datetime import datetime

class ConvertDateTime():
    pass

    '''
    The constructor
    @param dateTime: the dateTime string input
    '''
    def __init__(self, dateTime):
        self.dateTime=dateTime
    
    '''
    @return convD: converted value in date format
    '''
    def getDate(self):
        dateTime=self.dateTime
        d,t=dateTime.split('T')
        dy,dm,dd=d.split('-')
        convD=datetime.strptime(dy+'-'+dm+'-'+dd, "%Y-%m-%d")
        return convD
        
        