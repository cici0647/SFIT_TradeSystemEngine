'''
Created on 2015-5-7

@author: lu.siqiao
'''
import cx_Oracle

class GetDataFromSync(object):
    def __enter__(self):
        connStr = 'sync/oracle@192.168.24.108/tradeTester'
        self.__db__ = cx_Oracle.Connection(connStr)
        self.__cursor__ = self.__db__.cursor()
        return self 
  
    def __exit__(self, type, value, traceback):
        self.__db__.close()
        
        
    def getData(self,table):
        sqlStr = "Select * FROM " + str(table)
        self.__cursor__.execute(sqlStr)
        return self.__cursor__.fetchall()
    
class InsertDataToMDB(object):
    def __enter__(self):
        #connStr = 'mdb/oracle@192.168.24.108/tradeTester'
        connStr = 'Edwin/oracle@127.0.0.1/orcl'
        self.__db__ = cx_Oracle.Connection(connStr)
        self.__cursor__ = self.__db__.cursor()
        return self 
  
    def __exit__(self, type, value, traceback):
        self.__db__.close()
        
    def cleanData(self,table):
        sqlStr = "Truncate table " + str(table)
        self.__cursor__.execute(sqlStr)
        self.__db__.commit()
        
    def insertData(self,table1,table2):
        self.table1 = table1
        self.table2 = table2
        with GetDataFromSync() as GetSyncData:
            dataList = (GetSyncData.getData(table1))
            #print dataList
            i = 0
            for data in dataList:
                sqlstr = "insert into "+table2+ " (TRADINGDAY, SETTLEMENTGROUPID, SETTLEMENTID, PREOPENINTEREST, INSTRUMENTID ,TID) values (:tradeingDay, :settlementGroupID, :settlementID, :preopenInterest, :instrumentID, :tid)"
                #print 'sqlStr:',  sqlstr
                valdict = {'tradeingDay':data[0], 'settlementGroupID':data[1], 'settlementID':data[2], 'preopenInterest':data[6], 'instrumentID':data[21], 'tid':i+1}
                #print valdict
                self.__cursor__.execute(sqlstr, valdict)
                self.__db__.commit()
                i += 1

        
if __name__ =="__main__":
    table1 = 'T_MARKETDATA'
    table2 = 'MARKETDATA'
    with InsertDataToMDB() as syncToMDB:
        syncToMDB.cleanData(table2)
        syncToMDB.insertData(table1, table2)
    
            