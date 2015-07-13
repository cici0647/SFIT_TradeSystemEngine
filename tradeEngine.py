#! /usr/bin/env python
#coding=gbk
'''
Created on 2015-4-20
@author: kong.lihua

modify on 2015-5-11
@author: zhu.jing
增加回调

modify on 2015-5-21
@author: zhu.jing
rtn和rsp回调分开

modify on 2015-5-28
@author: zhu.jing
调用公有流私有流功能
使用sysLogger功能
'''
from mockData import MockData
from impl.orderProcessor import OrderProcessor
from impl.marketdataProcessor import MarketDtProcessor
from dbAction.syncToMDB import InsertDataToMDB
import copy
import sysLogger

class TradeEngine(object):

    def __init__(self, realm):        
        self.server = realm
        
        self.mockdata = MockData()
        self.orderProc = OrderProcessor()
        self.marketProc = MarketDtProcessor()
    
        self.orderProc.resetSequence('ORDERSYSID_AUTOINC_SEQ')
        self.orderProc.resetSequence('TRADESYSID_AUTOINC_SEQ')
        
        with InsertDataToMDB() as syncToMDB:
            #syncToMDB.cleanData('MARKETDATA')
            syncToMDB.cleanData('T_ORDERS')
            syncToMDB.cleanData('T_TRADERECORD')
            syncToMDB.cleanData('T_ORDERBOOKLIST')
            syncToMDB.insertData('T_MARKETDATA', 'MARKETDATA')
            sysLogger.LOGGER.info('sync data have finished')            
        
    def onLogin(self, username):
        self.server.privateSent(self.mockdata.onLogin, username)
        
    def onLogout(self, username):
        self.server.privateSent(self.mockdata.onLogout, username)           
                
    def ReqOrderInsert(self, data):
        self.currentUser = data.get('UserID')
        result = self.orderProc.orderInsert(self.callback, data)
        self.mockdata.onRspOrderInsert['Struct'].update(data)
        return self.mockdata.onRspOrderInsert
    
    def ReqOrderCancel(self, data):
        self.server.privateSent(self.mockdata.onLogout, self.currentUser)
        #self.remote.callRemote("print", self.mockdata.onRspOrderInsert)
        result = self.orderProc.orderInsert(self.callback, data)
        
        return True
    
    def ReqMarketData(self):
        data = self.marketProc.selectAll()
        #self.remote.callRemote("print", data)
        self.server.publicSent(data)
        
        
    def callback(self, rtnData):
        if rtnData['CallbackFunc'] == 'onRtnOrder':
            rtnMsg = self.mockdata.onRtnOrder
            rtnMsg['Struct'] = rtnData['Struct']
            #self.remote.callRemote("print", rtnMsg)
            self.server.groupSent(rtnMsg, self.currentUser)
        
        if rtnData['CallbackFunc'] == 'onRtnTrade':       #Trade completed
            rtnTrade = self.mockdata.onRtnTrade
            #print "result['tradeResult']: ", rtnData['Struct']
            rtnTrade['Struct']['TradeID'] = rtnData['Struct']['TradeSysID']
            rtnTrade['Struct']['Price'] = rtnData['Struct']['TradePrice']       
            #self.remote.callRemote("print", rtnTrade)
            self.server.groupSent(rtnTrade, self.currentUser)
        