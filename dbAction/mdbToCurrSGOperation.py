'''
Created on 2015-5-18

@author: lu.siqiao
'''
import cx_Oracle

class GetDataFromMdb(object):
    def __enter__(self):
        connStr = 'mdb/oracle@192.168.24.108/tradeTester'
        self.__db__ = cx_Oracle.Connection(connStr)
        self.__cursor__ = self.__db__.cursor()
        return self 
  
    def __exit__(self, type, value, traceback):
        self.__db__.close()
        
        
    def getData(self,table):
        sqlStr = "Select * FROM " + str(table)
        self.__cursor__.execute(sqlStr)
        return self.__cursor__.fetchall()
    
class InsertDataToCSO(object):
    def __enter__(self):
        connStr = 'currsgoperation/oracle@192.168.24.108/tradeTester'
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
        with GetDataFromMdb() as GetMdbData:
            dataList = (GetMdbData.getData(table1))
            print dataList
            for data in dataList:
                sqlstr = "insert into " + table2 + " (TRADINGDAY, SETTLEMENTGROUPID, SETTLEMENTID, ORDERSYSID, PARTICIPANTID, CLIENTID, USERID, INSTRUMENTID, ORDERPRICETYPE, DIRECTION, COMBOFFSETFLAG, COMBHEDGEFLAG, LIMITPRICE, VOLUMETOTALORIGINAL, TIMECONDITION, VOLUMECONDITION, MINVOLUME, CONTINGENTCONDITION, STOPPRICE, FORCECLOSEREASON, ORDERLOCALID, ISAUTOSUSPEND, BUSINESSLOCALID)  \
                values (:tradeingDay, :settlementGroupID, :settlementID, :ordersysID, :participantID, :clientID, :userID, :instrumentID, :orderpricetype, :direction, :comboffsetflag, :combhedgeflag, :limitprice, :volumetotaloriginal, :timecondition, :volumecondition, :minvolume, :contingentcondition, :stopprice, :forceclosereason, :orderlocalID, :isautosuspend, :businesslocalID)"
                print 'sqlStr:',  sqlstr
                print data
                valdict = {'tradeingDay':data[0], 'settlementGroupID':data[1], 'settlementID':data[2], 'ordersysID':data[3], 'participantID':data[4], 'clientID':data[5], 'userID':data[6], 'instrumentID':data[7], 'orderpricetype':data[8], 'direction':data[9], 'comboffsetflag':data[10], 'combhedgeflag':data[11], 'limitprice':data[12], 'volumetotaloriginal':data[13], 'timecondition':data[14], 'volumecondition':data[16], 'minvolume':data[17], 'contingentcondition':data[18], 'stopprice':data[19], 'forceclosereason':data[20], 'orderlocalID':data[21], 'isautosuspend':data[22], 'businesslocalID':data[39]}
                print valdict
                self.__cursor__.execute(sqlstr, valdict)
                self.__db__.commit()
                
if __name__ =="__main__":
    table1 = 'T_ORDERS'
    table2 = 'T_ORDER'
    with InsertDataToCSO() as syncToCSO:
        syncToCSO.cleanData(table2)
        syncToCSO.insertData(table1, table2)
                

        