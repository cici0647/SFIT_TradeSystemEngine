'''
Created on 2015-4-23

@author: kong.lihua
'''
import sys
sys.path.append(r'../dbAction')
# from dbAction.orders import Orders
# from dbAction.orderAction import OrderAction
# from dbAction.defaultData import Direction
from dictVerify import DictVerify
from wx.lib.pubsub.utils.misc import Callback

#from dbAction.rule import Rule, RuleList, InsertOrder, TradeOrder, SavePoint, CheckFunds

from orders import Orders
from orderAction import OrderAction
from defaultData import Direction
from rule import Rule, RuleList, InsertOrder, TradeOrder, SavePoint, CheckFunds

class OrderProcessor(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.dictVerify = DictVerify()
        
    def orderInsert(self, callback, orderDict):
        orderDict['InstrumentID'] = orderDict['InstrumentID'].ljust(30)
        return self.tradeLogic(orderDict, callback)
        
    def withdrawOrder(self, order):
        with OrderAction() as orderAction:
            orderAction.withdraw(order.get('OrderSysID'))
            
            return (True, order)
        
    def resetSequence(self, seqName):
        with Orders() as order:
            order.resetSequence(seqName)
    
    def savePoint(self, order, pointName):
        return SavePoint(order, pointName)
    
    def checkOrder(self, orderDict, order):
        pass
#         result = self.dictVerify.verifyAll(orderDict, 'T_ORDERS')
#         if result[0] == False:
#             return result

    def insertOrder(self, orderDict, callback, order, rollBackPoint):
        return InsertOrder(orderDict, callback, order, rollBackPoint)
   
    def tradeOrder(self, orderDict, callback, order, rollBackPoint):
        return TradeOrder(orderDict, callback, order, rollBackPoint)
   
    def checkFunds(self, orderDict, order):
        checkFundsObj = CheckFunds()
        return checkFundsObj
        
    def checkPosition(self, orderDict, order):
        return order.checkPosition(orderDict)
        
    
    def modifyFunds(self, orderDict, order):
        return order.modifyFunds(orderDict)
        
    
    def modifyPosition(self, orderDict, order):
        return order.modifyPosition(orderDict)
        
    
    def modifyTradePosition(self, orderDict, order):
        return order.modifyTradePosition(orderDict)
        
        
    def tradingRtn(self, tradeSysID, order, callback):
        tradeResult = order.selectTradeRecord(tradeSysID)
        
        rtnTradeBid = {}
        rtnTradeBid['TradeID'] = tradeResult['TradeSysID']
        rtnTradeBid['Price'] = tradeResult['TradePrice']
        rtnTradeBid['OrderSysID'] = tradeResult['OrderSysID_Bid']
        tradeRtnBid = {'CallbackFunc':'onRtnTrade','Struct':rtnTradeBid}
        callback(tradeRtnBid)
        
        rtnTradeAsk = {}
        rtnTradeAsk['TradeID'] = tradeResult['TradeSysID']
        rtnTradeAsk['Price'] = tradeResult['TradePrice']
        rtnTradeAsk['OrderSysID'] = tradeResult['OrderSysID_Ask']
        
        tradeRtnAsk = {'CallbackFunc':'onRtnTrade','Struct':rtnTradeAsk}
        callback(tradeRtnAsk)
        
    def tradeLogic(self, orderDict, callback):
        with Orders() as order:
            order.__db__.begin()
            tradeLogicBegin = 'tradeLogicBegin'
            self.savePoint(order, tradeLogicBegin)
            
            tradeOrderPoint = 'tradeOrderPoint'
            ruleListAll = [
                           self.checkFunds(orderDict, order), 
                           self.insertOrder(orderDict, callback, order, tradeLogicBegin),
                           self.savePoint(order, tradeOrderPoint),
                           self.tradeOrder(orderDict, callback, order, tradeOrderPoint)
                           ]
            ruleListObject = RuleList()

            for rule in ruleListAll:
                ruleListObject.addRule(rule)
                
            ruleListObject.executeRuleList()
            
            order.__db__.commit()
           
if __name__ == '__main__':
    # ORDERSYSID, USERID, ORDERLOCALID, INSTRUMENTID, DIRECTION, LIMITPRICE, VOLUMETOTALORIGINAL
    orderSysID = '000000000010'
    userID = '000000000000010'
    orderLocalID = '000000000010'
    instrumentID = 'AL1601                        '
    direction = '1'
    limitPrice = 2000
    volumeTotalOriginal = 10
    
    
    tradingDay = '20150423'
    settlementGroupID = '00000001'
    settlementID = 1
      
    orderDict = {
                   'OrderSysID':orderSysID,
                   'UserID':userID,
                   'OrderLocalID':orderLocalID,
                   'InstrumentID':instrumentID,
                   'Direction':direction,
                   'LimitPrice':limitPrice,
                   'VolumeTotalOriginal':volumeTotalOriginal,
                   'TradingDay':tradingDay,
                   'SettlementGroupID':settlementGroupID,
                   'SettlementID':settlementID,
                }
    orderDict= {
             'ContingentCondition': '1', 
             'IsAutoSuspend': 0, 
             'UserID': '0017cac', 
             'LimitPrice': 16400, 
             'Direction': '1', ######################
             'ParticipantID': '0017', 
             'VolumeTotalOriginal': 1, 
             'SettlementGroupID': '00000001', 
             'ClientID': '00000017', 
             'OrderPriceType': '2', 
             'TimeCondition': '3', 
             'OrderSysID': '000000000012', ##################
             'CombOffsetFlag': '0', 
             'StopPrice': 0, 
             'InstrumentID': 'al1208                        ', 
             'MinVolume': 0, 
             'SettlementID': 1, 
             'ForceCloseReason': '0', 
             'TradingDay': '20150423', 
             'CombHedgeFlag': '1', 
             'BusinessLocalID': 0, 
             'GTDDate': '', 
             'OrderLocalID': 'smok00000804', 
             'BusinessUnit': '', 
             'VolumeCondition': '1'}
    orderProcessor = OrderProcessor()
    #print orderProcessor.orderCheck()
    def callback_print(rtn):
        print 'call back print: ', rtn

    print orderProcessor.orderInsert(callback_print, orderDict)

                  
