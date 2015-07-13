#! /usr/bin/env python
#coding=gbk
'''
Created on 2015-4-21

@author: liang.ji

调用方法：
        dictVerify=DictVerify()
        if dictVerify.verifyAll(order,'T_ORDERS') == 'success'
        ...
'''
import cx_Oracle
import re

class DictVerify:
    def __enter__(self):
        connStr = 'MDB/oracle@192.168.24.108/tradeTester'
        self.__db__ = cx_Oracle.Connection(connStr)
        self.__cursor__ = self.__db__.cursor()
        return self 
    
    def __exit__(self, type, value, traceback): 
        self.__db__.close()
    
    def upperOrder(self,inputDict):
        upperOrder={}
        for key in inputDict:
            upperOrder[key.upper()]=inputDict[key]
        return upperOrder
    
    def verifyAll(self, inputDict,tableName, cursor = None):
        if cursor == None:
            connStr = 'MDB/oracle@192.168.24.108/tradeTester'
            self.__db__ = cx_Oracle.Connection(connStr)
            self.__cursor__ = self.__db__.cursor()
            
        verifResult = self.verifyIsNotNull(inputDict,tableName)
#         if verifResult != 'success':
        if verifResult != (True, {'errorMessage':0}):
            if cursor == None:
                self.__db__.close()
            return verifResult
        verifResult = self.verifyDataType(inputDict,tableName)
        if verifResult != (True, {'errorMessage':0}):
            if cursor == None:
                self.__db__.close()
            return verifResult
        
        if cursor == None:
            self.__db__.close()        
        return (True, {'errorMessage':0})
        

                
        
    def verifyDataType(self, inputDict,tableName):
        inputDict = self.upperOrder(inputDict)
        sqlStr="""select column_name,data_type,DATA_LENGTH From user_tab_columns where table_name=upper(:1)
        """
        self.__cursor__ .execute(sqlStr,(tableName,))
        result = self.__cursor__ .fetchall()
        count = self.__cursor__ .rowcount 
#         print count#,result
        if count != 0:
            for row in result:
                columnData=inputDict.get(row[0])
                if columnData != None:
                    if row[2] < len(str(columnData)):
#                         return 'overSizeError'
                        return (False, {'errorMessage':1})
                
                    if row[1]in('CHAR','VARCHAR2','NVARCHAR2','LONG'):
                        try:
                            str(columnData)
                        except Exception, e:  
#                             return 'dataTypeError' 
                            return (False, {'errorMessage':1})
                    elif row[1]=='NUMBER':
                        try:
                            int(columnData)
                        except Exception, e:  
#                             return 'dataTypeError' 
                            return (False, {'errorMessage':1})   
                    elif row[1]=='FLOAT':
                        try:
                            float(columnData)
                        except Exception, e:  
#                             return 'dataTypeError' 
                            return (False, {'errorMessage':1})   
#                     elif row[1]=='DATE':
#                         try:
#                             datetime.datetime(order.get(row[0]))
#                         except Exception, e:  
#                             return 'dataTypeError' 
        return (True, {'errorMessage':0})
    
                    
        
    def verifyIsNotNull(self, inputDict,tableName):
        inputDict = self.upperOrder(inputDict)
        sqlStr="""select constraint_name, search_condition from user_constraints where table_name=upper(:1) 
        """
        self.__cursor__ .execute(sqlStr,(tableName,))
        result = self.__cursor__ .fetchall()
#         print result
        count = self.__cursor__ .rowcount 
#         print count#,result
        if count != 0:
            for row in result:
#                 print row
                if row[1] != None and row[1].index('IS NOT NULL'):
                    columnName=re.findall(r'\"([^"]+)\"', row[1])[0]
                    if(inputDict.get(columnName) == None):
#                         return 'notNullError'
                        return (False, {'errorMessage':1})  
            return (True, {'errorMessage':0})
        else:
            return (True, {'errorMessage':0})
if __name__ == '__main__':
#     with DictVerify() as dictVerify:
        
        orderSysID = '000000000003'
        userID = '000000000000001'
        orderLocalID = '000000000003'
        instrumentID ='AL1601                        '
        direction = '1'
        limitPrice = 2000
        volumeTotalOriginal = 10
        
        order = {'OrderSysID':orderSysID, 'UserID':userID, 
                       'OrderLocalID':orderLocalID, 'InstrumentID':instrumentID,
                       'Direction':direction, 'LimitPrice':limitPrice,
                       'VolumeTotalOriginal':volumeTotalOriginal}
#         print dictVerify.verifyIsNotNull(order,'T_ORDERS');
#         print dictVerify.verifyDataType(order,'T_ORDERS');

        dictVerify=DictVerify()
        print dictVerify.verifyAll(order,'T_ORDERS');
