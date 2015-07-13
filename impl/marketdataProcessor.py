'''
Created on 2015-4-28

@author: kong.lihua
'''
#import sys; sys.path.append(r'../dbAction')
from dbAction.orders import Orders
from dbAction.defaultData import Direction
from dbAction.marketData import MarketData
from dictVerify import DictVerify


class MarketDtProcessor(object):
    '''
    classdocs
    '''


    def __init__(self):
        dictVerify=DictVerify()
       
    def selectAll(self):
        with MarketData() as md:
            result = md.SelectMarketData()
        
        return result
    
        