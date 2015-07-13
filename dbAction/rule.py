import sysLogger
from defaultData import ReqOrderInsert_d, OrderBookList_d, TradeRecord_d, Direction

class Rule(object):
    ruleName = 'rule'
    def __init__(self):
        self.name = ''
    def executeRule(self):
        return True

class RuleList(object):
    def __init__(self):
        self.ruleList = []
        
    def addRule(self, rule):
        self.ruleList.append(rule)
        
    def executeRuleList(self):
        for rule in self.ruleList:
            if rule.executeRule():
                print rule.ruleName + ' Pass.'
            else:
                print rule.ruleName + ' Fail.'
                break

class InsertOrder(Rule):
    ruleName = 'insertOrder'
    def __init__(self, orderDict, callback, order, rollBackPoint):
        self.orderDict = orderDict
        self.callback = callback
        self.order = order
        self.rollBackPoint = rollBackPoint
        
        
    def executeRule(self):              
        insertOrderFlag = False
        #insert a new order into T_ORDERS.
        if self.order.insertOrder(self.orderDict, self.rollBackPoint):
            insertOrderFlag = True
            orderRtn = {'CallbackFunc':'onRtnOrder','Struct':self.orderDict}
            sysLogger.LOGGER.info('orderRtn: ', orderRtn)
            print 'orderRtn: ', orderRtn
            self.callback(orderRtn)
        else:
            sysLogger.LOGGER.info('insert order error.')
            print 'insert order error.'

        return insertOrderFlag

class TradeOrder(Rule):
    ruleName = 'tradeOrder'
    def __init__(self, orderDict, callback, order, rollBackPoint):
        self.orderDict = orderDict
        self.callback = callback
        self.order = order
        self.rollBackPoint = rollBackPoint
        
        
    def executeRule(self):   
        tradeOrderFlag = False
        opponentOrderList = self.order.selectFromOrderBookList(self.orderDict)
        
        if len(opponentOrderList) == 0:
            self.order.insertOrderBookList(self.orderDict)
            tradeOrderFlag = True
        elif len(opponentOrderList) > 0:
            volume = self.orderDict['VolumeTotalOriginal']
            while volume > 0 and len(opponentOrderList) > 0:
                if volume > opponentOrderList[0][6]:
                    pass
                elif volume < opponentOrderList[0][6]:
                    pass                 
                else: 
                    # volume == opponentOrderList[0][6]
                    # trading price equal to  bid price
                    if self.orderDict['Direction'] == Direction.ASK:
                        orderSysIDAsk = self.orderDict['OrderSysID']
                        orderSysIDBid = opponentOrderList[0][0]
                        TradePrice = opponentOrderList[0][5]
                    elif self.orderDict['Direction'] == Direction.BID:
                        orderSysIDAsk = opponentOrderList[0][0]
                        orderSysIDBid = self.orderDict['OrderSysID']
                        TradePrice = self.orderDict['LimitPrice']
                    else:
                        sysLogger.LOGGER.info('Direction error!')
                    
                    TradeSysID = self.order.getTradeSysIDIncrNumber()
                    tradeRecord = {
                              'TradeSysID':TradeSysID,
                              'OrderSysID_Bid':opponentOrderList[0][0],
                              'OrderSysID_Ask':self.orderDict['OrderSysID'],
                              'InstrumentID':self.orderDict['InstrumentID'],
                              'TradePrice':TradePrice,
                              'TradeVolume':volume,
                              }
                    tradeSysID = self.order.insertRecordIntoTradeRecord(tradeRecord)
                    
                    if tradeSysID:
                        # delete the record in the T_ORDERBOOKLIST
                        self.order.deletRecordInOrderBookList(opponentOrderList[0][0])  # ORDERSYSID
                        volume = 0
                        tradeOrderFlag = True
                        
                        #trading Rtn
                        tradeResult = self.order.selectTradeRecord(tradeSysID)

                        rtnTradeBid = {}
                        rtnTradeBid['TradeID'] = tradeResult['TradeSysID']
                        rtnTradeBid['Price'] = tradeResult['TradePrice']
                        rtnTradeBid['OrderSysID'] = tradeResult['OrderSysID_Bid']
                        tradeRtnBid = {'CallbackFunc':'onRtnTrade','Struct':rtnTradeBid}
                        self.callback(tradeRtnBid)
                        
                        rtnTradeAsk = {}
                        rtnTradeAsk['TradeID'] = tradeResult['TradeSysID']
                        rtnTradeAsk['Price'] = tradeResult['TradePrice']
                        rtnTradeAsk['OrderSysID'] = tradeResult['OrderSysID_Ask']
                        
                        tradeRtnAsk = {'CallbackFunc':'onRtnTrade','Struct':rtnTradeAsk}
                        self.callback(tradeRtnAsk)
                    else:
                        sysLogger.LOGGER.info('trading failure.')
            if volume > 0:
                self.orderDict['VolumeTotalOriginal'] = volume
                self.order.insertOrderBookList(orderDict)
                tradeOrderFlag = True

        else:
            sysLogger.LOGGER.info('opponentOrderList length error.')

        return tradeOrderFlag

class SavePoint(Rule):
    ruleName = 'savePoint'
    def __init__(self, order, pointName):
        self.order = order
        self.pointName = pointName
        
        
    def executeRule(self):   
        try:
            self.order.__cursor__.execute('savepoint %s' % self.pointName)
            return True
        except Exception as e:
            sysLogger.LOGGER.info(e)
            return False
    
class CheckFunds(Rule):
    pass

if __name__ == '__main__':
    my = Rule()
    print my.ruleName
    def myfun():
        for i in range(5):
            print i
            if i == 3:
                break
    print myfun()
        
        
        
        