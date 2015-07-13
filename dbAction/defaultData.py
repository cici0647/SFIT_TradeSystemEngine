#! /usr/bin/env python
#coding=gbk
'''
Created on 2015-4-20

@author: cai.shijie
'''

def enum(**enums):
    return type('DIRECTION', (), enums)
Direction = enum(BID='0', ASK='1')

userid = 'sun.wei'
clientid='00000017'
participantid='0017'
sysid=''
businessunit=''
businesslocalid=0

tradingDay = '20150423'
settlementGroupID = '00000001'
settlementID = 1

ReqOrderInsert_d={  
                    'UserID':userid,
                    'InstrumentID':'al1211',
                    'VolumeTotalOriginal':1,
                    'LimitPrice':17000,
                    'Direction':'1',
                    'OrderLocalID':'00000000009',#���ر����ţ�Ψһ��
                    'OrderSysID':sysid,       #ϵͳ�������ڴ���д��Ч��
                    'TradingDay':tradingDay,
                    'SettlementGroupID':settlementGroupID,
                    'SettlementID':settlementID,  
                    
                    'TimeCondition':'3',        #��Ч�����ͣ�3 ������Ч
                    'GTDDate':'',               #GTD����
                    'VolumeCondition':'1',      #�ɽ������ͣ�1 �κ�����
                    'MinVolume':0,              #��С�ɽ�����0
                    'ContingentCondition':'1',  #����������1 ����
                    'StopPrice':0,              #ֹ���
                    'ForceCloseReason':'0',     #ǿƽԭ�����ͣ�0 ��ǿƽ
                    'IsAutoSuspend':0,          #�Զ������־                  
                    'OrderPriceType':'2',
                    'BusinessUnit':businessunit,
                    'BusinessLocalID':businesslocalid,
                    
                    'ParticipantID': '0017',
                    'ClientID': '00000017',
                    'CombOffsetFlag': '0',
                    'CombHedgeFlag': '1',
                    }
                         
OrderBookList_d ={'OrderSysID':'1',
                  'UserID': userid,
                  'OrderLocalID': '1',
                  'InstrumentID': 'al1211                        ',
                  'Direction': '1',
                  'LimitPrice': 1,
                  'VolumeTotalOriginal': 1,
                  'TradingDay': tradingDay,
                  'SettlementGroupID': settlementGroupID,
                  'SettlementID': settlementID,}

tradeSysID =''
orderSysID_Bid= ''
orderSysID_Ask=''
instrumentID=''
tradePrice=''
tradeVolume=''
TradeRecord_d={
              'TradeSysID':tradeSysID,
              'OrderSysID_Bid':orderSysID_Bid,
              'OrderSysID_Ask':orderSysID_Ask,
              'InstrumentID':instrumentID,
              'TradePrice':tradePrice,
              'TradeVolume':tradeVolume,   
              'TradingDay':tradingDay,
              'SettlementGroupID':settlementGroupID,
              'SettlementID':settlementID,
               }
a= {"TradeType": "\u0000", "HedgeFlag": "1", "TradeTime": "21:57:20", "AccountID": "", 
         "Direction": "1", "OffsetFlag": "0", "Price": 16400.0, "SettlementGroupID": "00000001", 
         "ClientID": "00000017", "Volume": 1, "OrderSysID": "           6", "ClearingPartID": "0017", 
         "InstrumentID": "al1208", "SettlementID": 1, "UserID": "0017cac", "TradingDay": "20120112", 
         "ParticipantID": "0017", "BusinessLocalID": 0, "OrderLocalID": "smok00000711", "TradeID": "           3", 
         "BusinessUnit": "", "PriceSource": "\u0000", "TradingRole": "\u0000"}
ReqOrderAction_d={'UserID':userid,
                    'InstrumentID':'al1211',
                    'VolumeTotalOriginal':1,'LimitPrice':17000,'Direction':'1',
                    'OrderLocalID':'00000000009',#���ر����ţ�Ψһ��
                    #'TimeCondition':'3',        #��Ч�����ͣ�3 ������Ч
                    #'GTDDate':'',               #GTD����
                    #'VolumeCondition':'1',      #�ɽ������ͣ�1 �κ�����
                    #'MinVolume':0,              #��С�ɽ�����0
                    #'ContingentCondition':'1',  #����������1 ����
                    #'StopPrice':0,              #ֹ���
                    #'ForceCloseReason':'0',     #ǿƽԭ�����ͣ�0 ��ǿƽ
                    #'IsAutoSuspend':0,          #�Զ������־
                    'OrderSysID':sysid,       #ϵͳ�������ڴ���д��Ч��
                    #'OrderPriceType':'2',
                    #'BusinessUnit':businessunit,
                    #'BusinessLocalID':businesslocalid
                  }