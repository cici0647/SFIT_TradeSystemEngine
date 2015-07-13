'''
Created on 2015-4-23

@author: kong.lihua
'''
import time


class MockData(object):
    '''
    classdocs
    '''


    def __init__(self):
        localtime = time.strftime('%Y%m%d-%H:%M:%S',time.localtime(time.time()))
        
        self.onFront = {"SessionID": "Default", "Systime": localtime, "CallbackFunc": "OnFrontConnected"}
        self.onLogin = {"SessionID": "Default", "Systime": localtime, "Struct": {"ActionDay": "20120111", "PrivateFlowSize": 15, "ErrorMsg": "", "UserFlowSize": 15, "UserID": "0017cac", "LoginTime": "22:58:43", "DataCenterID": 1, "TradingDay": "20120112", "RequestID": 1, "MaxOrderLocalID": "smok00000711", "TradingSystemName": "Trading System", "IsLast": 1, "ErrorID": 0, "ParticipantID": "0017"}, "CallbackFunc": "OnRspUserLogin"}
        self.onRspOrderInsert = {"SessionID": "Default", "Systime": localtime, "Struct": {"ContingentCondition": "1", "CombOffsetFlag": "0", "UserID": "0017cac", "LimitPrice": 16400.0, "Direction": "0", "ParticipantID": "0017", "VolumeTotalOriginal": 1, "ClientID": "00000017", "OrderPriceType": "2", "TimeCondition": "3", "OrderSysID": "000000000006", "IsAutoSuspend": 0, "StopPrice": 0.0, "InstrumentID": "al1208", "MinVolume": 0, "ForceCloseReason": "0", "ErrorID": 0, "CombHedgeFlag": "1", "BusinessLocalID": 0, "GTDDate": "", "OrderLocalID": "smok00000712", "BusinessUnitason": "0", "ErrorID": 0, "CombHedgeFlag": "1", "BusinessLocalID": 0, "GTDDate": "", "OrderLocalID": "smok00000712", "BusinessUnit": "", "ErrorMsg": "Success", "VolumeCondition": "1", "RequestID": 1, "IsLast": 1}, "CallbackFunc": "OnRspOrderInsert"}
        self.onPackageStart = {"SessionID": "Default", "Systime": localtime, "Struct": {"nTopicID": 2, "nSequenceNo": 1}, "CallbackFunc": "OnPackageStart"}
        self.onPackageEnd = {"SessionID": "Default", "Systime": localtime, "Struct": {"nTopicID": 2, "nSequenceNo": 1}, "CallbackFunc": "OnPackageEnd"}
        self.onRtnOrder = {"SessionID": "Default", "Systime": localtime, "Struct": {"ContingentCondition": "1", "ActiveUserID": "0017cac", "VolumeTraded": 0, "CombOffsetFlag": "0", "UserID": "0017cac", "LimitPrice": 16400.0, "Priority": 0, "Direction": "0", "ActiveTime": "", "ParticipantID": "0017", "VolumeTotalOriginal": 1, "SettlementGroupID": "", "ClientID": "00000017", "VolumeTotal": 1, "OrderPriceType": "2", "TimeCondition": "3", "OrderStatus": "3", "OrderSysID": "           1", "IsAutoSuspend": 0, "StopPrice": 0.0, "InstrumentID": "al1208", "ActionDay": "20120111", "MinVolume": 0, "SettlementID": 0, "ForceCloseReason": "0", "OrderType": "\u0000", "UpdateTime": "", "TradingDay": "", "CancelTime": "", "OrderSource": "\u0000", "InsertTime": "21:56:50", "GTDDate": "", "ClearingPartID": "", "CombHedgeFlag": "1", "TimeSortID": 0, "BusinessLocalID": 0, "SuspendTime": "", "OrderLocalID": "smok00000706", "BusinessUnit": "", "InsertDate": "20120112", "VolumeCondition": "1"}, "CallbackFunc": "OnRtnOrder"}
        self.onRtnTrade = {"SessionID": "Default", "Systime": localtime, "Struct": {"TradeType": "\u0000", "HedgeFlag": "1", "TradeTime": "21:57:20", "AccountID": "", "Direction": "1", "OffsetFlag": "0", "Price": 16400.0, "SettlementGroupID": "00000001", "ClientID": "00000017", "Volume": 1, "OrderSysID": "           6", "ClearingPartID": "0017", "InstrumentID": "al1208", "SettlementID": 1, "UserID": "0017cac", "TradingDay": "20120112", "ParticipantID": "0017", "BusinessLocalID": 0, "OrderLocalID": "smok00000711", "TradeID": "           3", "BusinessUnit": "", "PriceSource": "\u0000", "TradingRole": "\u0000"}, "CallbackFunc": "OnRtnTrade"}
        self.onRtnInstrument = {"SessionID": "Default", "Systime": localtime, "Struct": {"InstrumentID": "ag1204", "InstrumentName": "ag1204", "StrikePrice": 1.7976931348623157e+308, "ProductGroupID": "ag", "CurrencyID": "CNY", "DeliveryYear": 2012, "SettlementGroupID": "00000001", "UnderlyingMultiple": 1.0, "AdvanceMonth": 1, "OptionsType": "0", "VolumeMultiple": 15, "PositionType": "2", "ProductClass": "1", "ProductID": "ag_f", "DeliveryMonth": 4, "UnderlyingInstrID": "ag"}, "CallbackFunc": "OnRtnInsInstrument"}
        self.error = {"SessionID": "Default", "Systime": localtime, "Struct": {"ContingentCondition": "1", "CombOffsetFlag": "0", "UserID": "sun.wei", "LimitPrice": 4899.0, "Direction": "0", "ParticipantID": "1017", "VolumeTotalOriginal": 1, "ClientID": "00000017", "OrderPriceType": "2", "TimeCondition": "3", "OrderSysID": "", "IsAutoSuspend": 0, "StopPrice": 0.0, "InstrumentID": "wr1205", "MinVolume": 0, "ForceCloseReason": "0", "ErrorID": 3, "CombHedgeFlag": "1", "BusinessLocalID": 0, "GTDDate": "", "OrderLocalID": "300100000001", "BusinessUnit": "", "ErrorMsg": "Cannot found participants", "VolumeCondition": "1", "RequestID": 1, "IsLast": 1}, "CallbackFunc": "OnRspOrderInsert"}