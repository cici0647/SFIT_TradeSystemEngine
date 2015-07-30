#! /usr/bin/env python
#coding=gbk
'''
Created on 2015-4-19

@author: cai.shijie
''' 
import cx_Oracle
import copy
import sys
sys.path.append(r'../')
import sysLogger

from defaultData import ReqOrderInsert_d, OrderBookList_d, TradeRecord_d, Direction

class Orders:
    def __enter__(self):
        try:
            #connStr = 'MDB/oracle@192.168.24.108/tradeTester'
            connStr = 'Edwin/oracle@127.0.0.1/orcl'
            self.__db__ = cx_Oracle.Connection(connStr)
            self.__cursor__ = self.__db__.cursor()
            #orderVerift
            #self.__orderVerify__ = OrderVerify(self.__cursor__)
        except Exception as e:
            print e    
        else: 
            return self 
  
    def __exit__(self, type, value, traceback):
        try:
            self.__db__.close()
        except Exception as e:
            print e 
        
    def resetSequence(self, seqName):
        dropSeqStr = 'drop sequence ' + seqName
        self.__cursor__.execute(dropSeqStr)
        

        createSeqStr = 'create sequence ' + seqName + \
                    '''
minvalue 1
maxvalue 999999999999
start with 1
increment by 1
cache 20
                    '''
        self.__cursor__.execute(createSeqStr)
    
    def getOrderSysIDIncrNumber(self):
        sqlStr = "select ORDERSYSID_AUTOINC_SEQ.nextval from all_sequences where sequence_name= :seqName"
        self.__cursor__.execute(sqlStr, seqName='ORDERSYSID_AUTOINC_SEQ')
        nextVal=self.__cursor__.fetchone()
        return nextVal[0]
    
    def insertOrder(self, order, rollBackPoint):
        try:
            orderSysID = self.getOrderSysIDIncrNumber()
            order['OrderSysID'] = orderSysID
            
            sqlStr = '''
                        INSERT INTO T_ORDERS (
                        ORDERSYSID, USERID, ORDERLOCALID, INSTRUMENTID, DIRECTION, 
                        LIMITPRICE, VOLUMETOTALORIGINAL, TRADINGDAY, SETTLEMENTGROUPID, SETTLEMENTID, 
                        TIMECONDITION, GTDDATE, VOLUMECONDITION, MINVOLUME, CONTINGENTCONDITION,
                        STOPPRICE, FORCECLOSEREASON, ISAUTOSUSPEND, ORDERPRICETYPE, BUSINESSUNIT,
                        BUSINESSLOCALID, PARTICIPANTID, CLIENTID, COMBOFFSETFLAG, COMBHEDGEFLAG)
                        VALUES (
                        :OrderSysID, :UserID, :OrderLocalID, :InstrumentID, :Direction, 
                        :LimitPrice, :VolumeTotalOriginal, :TradingDay, :SettlementGroupID, :SettlementID, 
                        :TimeCondition, :GTDDate, :VolumeCondition, :MinVolume, :ContingentCondition,
                        :StopPrice, :ForceCloseReason, :IsAutoSuspend, :OrderPriceType, :BusinessUnit,
                        :BusinessLocalID, :ParticipantID, :ClientID, :CombOffsetFlag, :CombHedgeFlag)
                     '''
            
            ReqOrderInsert_d.update(order)
            self.__cursor__.execute(sqlStr, ReqOrderInsert_d)
            self.__db__.commit()##########
            return True
        except Exception as e:
            self.__cursor__.execute('rollback to '+ rollBackPoint)
            sysLogger.LOGGER.info(e) 
            return False

    def selectOrder(self, orderSysID):
        sqlStr = '''
                    SELECT * FROM T_ORDERS WHERE ORDERSYSID = :orderSysIDSelect
                 '''
        self.__cursor__.execute(sqlStr, orderSysIDSelect=orderSysID)
        orderAttributeList = ['TradingDay', 'SettlementGroupID', 'SettlementID', 'OrderSysID', 'ParticipantID',
                              'ClientID', 'UserID', 'InstrumentID', 'OrderPriceType', 'Direction',
                              'CombOffsetFlag', 'CombHedgeFlag', 'LimitPrice', 'VolumeTotalOriginal', 'TimeCondition',
                              'GTDDate', 'VolumeCondition', 'MinVolume', 'ContingentCondition', 'StopPrice',
                              'ForceCloseReason', 'OrderLocalID', 'IsAutoSuspend', 'OrderSource', 'OrderStatus',
                              'OrderType', 'VolumeTraded', 'VolumeTotal', 'InsertDate', 'InsertTime',
                              'ActiveTime', 'SuspendTime', 'UpdateTime', 'CancelTime', 'ActiveUserID',
                              'Priority', 'TimeSortID', 'ClearingPartID', 'BusinessUnit', 'BusinessLocalID',
                              'ActionDay']
        orderValueList = self.__cursor__.fetchone()
        return dict(zip(orderAttributeList, orderValueList))
    
    def deletOrder(self, orderSysID): 
        try:
            sqlStr ="DELETE FROM ORDERS WHERE ORDERSYSID = :b_orderSysID"
            dictOrder = {'b_orderSysID': orderSysID}
            self.__cursor__.execute(sqlStr, dictOrder)
            self.__db__.commit()
        except Exception, e:
            print e
    
    ##########OrderBookList##########
    def insertOrderBookList(self, order):
        try:
            sqlStr = '''
                        INSERT INTO T_ORDERBOOKLIST (
                        ORDERSYSID, USERID, ORDERLOCALID, INSTRUMENTID, DIRECTION, 
                        LIMITPRICE, VOLUMETOTALORIGINAL, TRADINGDAY, SETTLEMENTGROUPID, SETTLEMENTID)
                        VALUES (
                        :OrderSysID, :UserID, :OrderLocalID, :InstrumentID, :Direction, 
                        :LimitPrice, :VolumeTotalOriginal, :TradingDay, :SettlementGroupID, :SettlementID)
                    '''
            
            dictOrder = {
                         'OrderSysID':order['OrderSysID'], 'UserID':order['UserID'], 'OrderLocalID':order['OrderLocalID'], 
                         'InstrumentID':order['InstrumentID'], 'Direction':order['Direction'], 'LimitPrice':order['LimitPrice'], 
                         'VolumeTotalOriginal':order['VolumeTotalOriginal'],
                        }
            OrderBookList_d.update(dictOrder)
    
            self.__cursor__.execute(sqlStr, OrderBookList_d)
        except Exception as e:
            self.__cursor__.execute('rollback to tradingBeginning')
            print e


    def selectFromOrderBookList(self, originalOrder):
        try:
            if isinstance(originalOrder, dict):
                #order by price
                if originalOrder['Direction'] == Direction.BID:
                    oppoDirection = Direction.ASK
                    sqlStr = '''SELECT * FROM T_ORDERBOOKLIST WHERE 
                    INSTRUMENTID=:instrumentID AND
                    DIRECTION=:oppoDirection AND 
                    LIMITPRICE<=:limitPrice ORDER BY LIMITPRICE ASC'''
                elif originalOrder['Direction'] == Direction.ASK:
                    oppoDirection = Direction.BID
                    sqlStr = '''SELECT * FROM T_ORDERBOOKLIST WHERE 
                    INSTRUMENTID=:instrumentID AND
                    DIRECTION=:oppoDirection AND 
                    LIMITPRICE>=:limitPrice ORDER BY LIMITPRICE DESC'''
                else:
                    print 'Direction is illegal!' 
                print type(Direction.ASK)
                self.__cursor__.execute(
                                        sqlStr, 
                                        instrumentID=originalOrder['InstrumentID'], 
                                        oppoDirection=oppoDirection, 
                                        limitPrice=originalOrder['LimitPrice']
                                        )
        
                return self.__cursor__.fetchall()
            else:
                print 'Parameter type error!'
        except Exception as e:
            #self.__cursor__.execute('rollback to tradingBeginning')
            print e 
            return []
    
    def updateVolumeOrderBookList(self, orderSysID, volumeTotalOriginal):
        #variable banding format or authority.
        sqlStr = "UPDATE T_ORDERBOOKLIST SET VOLUMETOTALORIGINAL = :volumeTotalOriginal WHERE ORDERSYSID = :orderSysID"
        dict_b = {'volumeTotalOriginal':volumeTotalOriginal, 'orderSysID':orderSysID}
        self.__cursor__.execute(sqlStr, dict_b)
        self.__cursor__.execute(sqlStr)
        self.__db__.commit()
        
    def deletRecordInOrderBookList(self, orderSysID):
        sqlStr ="DELETE FROM T_ORDERBOOKLIST WHERE ORDERSYSID = :b_orderSysID"
        dictOrder = {'b_orderSysID': orderSysID}
        self.__cursor__.execute(sqlStr, dictOrder)
        self.__db__.commit()
    
    ##########TradeRecord##########
    def getTradeSysIDIncrNumber(self):
        sqlStr = "select TRADESYSID_AUTOINC_SEQ.nextval from all_sequences where sequence_name= :seqName"
        self.__cursor__.execute(sqlStr, seqName='TRADESYSID_AUTOINC_SEQ')
        nextVal=self.__cursor__.fetchone()
        return nextVal[0]
    
    def insertRecordIntoTradeRecord(self, record):
        try:
            tradeSysID = self.getTradeSysIDIncrNumber()
            record['TradeSysID'] = tradeSysID
            sqlStr = '''
                        INSERT INTO T_TRADERECORD (
                        TRADESYSID, ORDERSYSID_BID, ORDERSYSID_ASK, INSTRUMENTID, TRADEPRICE, 
                        TRADEVOLUME, TRADINGDAY, SETTLEMENTGROUPID, SETTLEMENTID) 
                        VALUES (
                        :TradeSysID, :OrderSysID_Bid, :OrderSysID_Ask, :InstrumentID, :TradePrice, 
                        :TradeVolume, :tradingDay, :settlementGroupID, :settlementID)
                        '''
            TradeRecord_d.update(record)
            self.__cursor__.execute(sqlStr, TradeRecord_d)
            self.__db__.commit()
            return tradeSysID
        except Exception as e:
            self.__cursor__.execute('rollback to tradeLogicBegin')
            print e
            return None
    
    def selectTradeRecord(self, tradeSysID):
        sqlStr = '''
                    SELECT * FROM T_TRADERECORD WHERE TRADESYSID=:b_tradeSysID        
        '''
        self.__cursor__.execute(sqlStr, b_tradeSysID=tradeSysID)
        tradeRecordValueList = self.__cursor__.fetchone()
        #return tradeRecordValueList
        tradeRecordAttributeList = ['TradeSysID', 'OrderSysID_Bid', 'OrderSysID_Ask', 
                                    'InstrumentID', 'TradePrice', 'TradeVolume',
                                    'TradeVolume', 'TradingDay', 'SettlementGroupID']
        if tradeRecordValueList == None:
            return {}
        else:
            return dict(zip(tradeRecordAttributeList, tradeRecordValueList))
        
    #############Position##############
    def positionRecordExist(self, record):
        sqlStr = '''
                    SELECT * FROM T_PARTPOSITION WHERE
                    POSIDIRECTION =:PosiDirection AND
                    INSTRUMENTID =:InstrumentID AND
                    PARTICIPANTID =:ParticipantID
                '''
        searchRecord = copy.copy(record)
        searchRecord.pop('Position') #delete Position
        self.__cursor__.execute(sqlStr, searchRecord)

        if len(self.__cursor__.fetchall()) > 0:
            return True
        else:
            return False
    
    def insertPosition(self, record):
        sqlStr = '''INSERT INTO T_PARTPOSITION (POSIDIRECTION, POSITION, INSTRUMENTID, PARTICIPANTID)
                    VALUES (:PosiDirection, :Position, :InstrumentID, :ParticipantID)'''
        self.__cursor__.execute(sqlStr, record)
        self.__db__.commit()    
        #"UPDATE T_ORDERBOOKLIST SET VOLUMETOTALORIGINAL = :b_volumeTotalOriginal WHERE ORDERSYSID = :b_orderSysID"
    def updatePosition(self, record):
        sqlStr = '''
                    UPDATE T_PARTPOSITION SET POSITION = :Position + 
                    (
                    SELECT POSITION FROM T_PARTPOSITION WHERE
                    POSIDIRECTION = :PosiDirection AND
                    INSTRUMENTID = :InstrumentID AND
                    PARTICIPANTID = :ParticipantID
                    ) 
                    WHERE 
                    POSIDIRECTION = :PosiDirection AND
                    INSTRUMENTID = :InstrumentID AND
                    PARTICIPANTID = :ParticipantID
                 '''
        self.__cursor__.execute(sqlStr, record)
        self.__db__.commit()
    
    def insertTradingAccount(self, record):
        sqlStr = '''INSERT INTO T_TRADINGACCOUNT (ACCOUNTID, PREBALANCE, CURRMARGIN, AVAILABLE)
                    VALUES (:AccountID, :PreBalance, :CurrMargin, :Available)'''
        self.__cursor__.execute(sqlStr, record)
        self.__db__.commit()
    
    def modefiyTradingAccount(self, userID, turnOver):
        sqlSelectStr ='''SELECT CURRMARGIN, AVAILABLE FROM T_TRADINGACCOUNT WHERE ACCOUNTID=:AccountID'''
        self.__cursor__.execute(sqlSelectStr, AccountID=userID)
        currMargin, available = self.__cursor__.fetchone()
        print currMargin, available
        marginRate = 0.01
        deltaAccount = turnOver*marginRate
        currMargin = deltaAccount + currMargin
        available = available - deltaAccount
        print currMargin, available
        sqlUpdateStr = '''UPDATE T_TRADINGACCOUNT SET 
                          CURRMARGIN = :CurrMargin, AVAILABLE =:Available WHERE ACCOUNTID=:AccountID'''        
        updateDict = {
                      'ACCOUNTID': userID,
                      'CURRMARGIN': currMargin,
                      'AVAILABLE': available
                      }
        self.__cursor__.execute(sqlUpdateStr, updateDict)
        self.__db__.commit()
        
    def getCurrValueSeq(self):
        sqlStr = "select ORDERSYSID_AUTOINC_SEQ.currval from all_sequences where sequence_name= 'ORDERSYSID_AUTOINC_SEQ'"
        self.__cursor__.execute(sqlStr)
        nextVal=self.__cursor__.fetchone()
        return nextVal[0]
    
    def checkFunds(self, orderDict):
        #return True if checking funds pass, else return False
        return True
        
    def checkPosition(self, orderDict):
        #return True if checking position pass, else return False
        return True
    
    def modifyFunds(self, orderDict):
        try:
            #modify funds
            return True
        except Exception as e:
            self.__cursor__.execute('rollback to tradeLogicBegin')
            print e
            return False
        
    def modifyPosition(self, orderDict):
        try:
            #modify position
            return True
        except Exception as e:
            self.__cursor__.execute('rollback to tradeLogicBegin')
            print e
            return False
        
    def modifyTradePosition(self, orderDict):
        self.__cursor__.execute('savepoint beforeModifyTradePosition')
        
        
if __name__ == '__main__':
    with Orders() as order:
        orderSysID = '000000000001'
        userID = '000000000000001'
        orderLocalID = '000000000001'
        instrumentID ='AL1601                        '
        direction = '0'
        limitPrice = 2000
        volumeTotalOriginal = 10
        TradeSysID  = 0
        
        tradingDay = '20150423'
        settlementGroupID = '00000001'
        settlementID = 1
        
        orderDict= {
                 'ContingentCondition': '1', 
                 'IsAutoSuspend': 0, 
                 'UserID': '0017cac', 
                 'LimitPrice': 16400, 
                 'Direction': '1', 
                 'ParticipantID': '0017', 
                 'VolumeTotalOriginal': 1, 
                 'SettlementGroupID': '00000001', 
                 'ClientID': '00000017', 
                 'OrderPriceType': '2', 
                 'TimeCondition': '3', 
                 'OrderSysID': 14, 
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
        
        orderDict = {
                       'ContingentCondition': '1', 
#                      'CombOffsetFlag': '0', 
                       'UserID': '0017cac', 
                       'LimitPrice': 17000, 
                       'Direction': '1', 
#                      'ParticipantID': '0017', 
                       'VolumeTotalOriginal': 1, 
#                      'ClientID': '00000017', 
#                      'OrderPriceType': '2', 
#                      'TimeCondition': '3', 
                       'OrderSysID': 94, 
#                      'IsAutoSuspend': 0, 
#                      'StopPrice': 0, 
                       'InstrumentID': 'al1211                        ', 
#                      'MinVolume': 0, 
#                      'ForceCloseReason': '0', 
#                      'CombHedgeFlag': '1', 
#                      'BusinessLocalID': 0, 
#                      'GTDDate': '', 
                       'OrderLocalID': '1001', 
#                      'BusinessUnit': '', 
#                      'VolumeCondition': '1',

#                      'TradingDay': '20150423',
                       'SettlementGroupID': '00000001', 
                       'SettlementID': 1, 
                     }

        print order.insertOrder(orderDict, 'savaPoint')


