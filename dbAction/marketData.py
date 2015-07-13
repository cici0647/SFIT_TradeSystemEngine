#! /usr/bin/env python
#coding=gbk
'''
Created on 2015-4-23

@author: zhu.jing
'''
import cx_Oracle

connStr = 'mdb/oracle@192.168.24.108/tradeTester'

class MarketData:
    def __enter__(self):
        self.__db = cx_Oracle.Connection(connStr)
        self.__cursor = self.__db.cursor()
        return self 
    
    def __exit__(self, type, value, traceback): 
        self.__db.close()
    
    def UpdateMarketData(self):
        self.__cursor.execute ("select distinct instrumentid from t_traderecord")
        rows = self.__cursor.fetchall()       
        i = 0
        for row in rows:              
            #volume
            self.__cursor.execute ("select sum(tradevolume) from t_traderecord where instrumentid =:id group by instrumentid",id = row[i])
            vol =  self.__cursor.fetchone()            
            #highestprice
            self.__cursor.execute ("select max(tradeprice) from t_traderecord where instrumentid =:id group by instrumentid",id = row[i])
            max =  self.__cursor.fetchone()           
            #lowestprice
            self.__cursor.execute ("select min(tradeprice) from t_traderecord where instrumentid =:id group by instrumentid",id = row[i])
            min =  self.__cursor.fetchone()            
            #lastprice
            self.__cursor.execute ("select tradingday, settlementgroupid, settlementid, tradeprice from t_traderecord where instrumentid =:id order by tradesysid desc",id = row[i])
            new =  self.__cursor.fetchone()
                                
            self.__cursor.execute ("select * from marketdata where instrumentid =:id",id = row[i])
            onerow =  self.__cursor.fetchone()                   
            if onerow is None:
                sqlstr = "insert into marketdata (tradingday, settlementgroupid, settlementid, lastprice, preopeninterest, highestprice, lowestprice, volume, instrumentid, tid)  \
                    values (:day, :groupid, :sid, :price, :open, :high, :low, :vol, :id, :tid)"
                valdict = {'day':new[0], 'groupid':new[1], 'sid':new[2], 'price':new[3], 'open':new[3], 'high':max[0], 'low':min[0], 'vol':vol[0], 'id':row[i], 'tid':i+1}
                self.__cursor.execute(sqlstr, valdict)
                self.__db.commit() 
            else:
                sqlstr = "update marketdata set lastprice=:price, highestprice=:high, lowestprice=:low, volume=:vol  where instrumentid=:id"
                valdict = {'price':new[3], 'high':max[0], 'low':min[0], 'vol':vol[0], 'id':row[i]}
                self.__cursor.execute(sqlstr, valdict)
                self.__db.commit()
                
            i+=1
            
            
    def UpdateDepthMarketData(self):
        self.__cursor.execute ("select distinct instrumentid from t_traderecord")
        rows = self.__cursor.fetchall()       
        i = 0
        for row in rows:             
            #volume
            self.__cursor.execute ("select sum(tradevolume) from t_traderecord where instrumentid =:id group by instrumentid",id = row[0])
            vol =  self.__cursor.fetchone()            
            #highestprice
            self.__cursor.execute ("select max(tradeprice) from t_traderecord where instrumentid =:id group by instrumentid",id = row[0])
            max =  self.__cursor.fetchone()           
            #lowestprice
            self.__cursor.execute ("select min(tradeprice) from t_traderecord where instrumentid =:id group by instrumentid",id = row[0])
            min =  self.__cursor.fetchone()           
            #lastprice
            self.__cursor.execute ("select tradingday, settlementgroupid, settlementid, tradeprice from t_traderecord where instrumentid =:id order by tradesysid desc",id = row[0])
            new =  self.__cursor.fetchone()
                                
            self.__cursor.execute ("select * from depthmarketdata where instrumentid =:id",id = row[0])
            onerow =  self.__cursor.fetchone()                  
            if onerow is None:
                sqlstr = "insert into depthmarketdata (tradingday, settlementgroupid, settlementid, lastprice, preopeninterest, highestprice, lowestprice, volume, instrumentid, sequenceno)  \
                    values (:day, :groupid, :sid, :price, :open, :high, :low, :vol, :id, :no)"
                valdict = {'day':new[0], 'groupid':new[1], 'sid':new[2], 'price':new[3], 'open':new[3], 'high':max[0], 'low':min[0], 'vol':vol[0], 'id':row[0], 'no':i+1}
                self.__cursor.execute(sqlstr, valdict)
                self.__db.commit() 
            else:
                sqlstr = "update depthmarketdata set lastprice=:price, highestprice=:high, lowestprice=:low, volume=:vol  where instrumentid=:id"
                valdict = {'price':new[3], 'high':max[0], 'low':min[0], 'vol':vol[0], 'id':row[0]}
                self.__cursor.execute(sqlstr, valdict)
                self.__db.commit()
                
            #ask&bid ---- for depthmarketdata   
            self.__cursor.execute ("select limitprice, volumetotaloriginal from t_orderbooklist where instrumentid =:id and direction = '1' order by limitprice desc",id = row[i])
            bids =  self.__cursor.fetchall()
            self.__cursor.execute ("select limitprice, volumetotaloriginal from t_orderbooklist where instrumentid =:id and direction = '0' order by limitprice asc",id = row[i])
            asks =  self.__cursor.fetchall()
            n = 0
            for bid in bids:
                n+=1
                sqlstr = "update depthmarketdata set bidprice"+str(n)+"=:b, bidvolume"+str(n)+"=:v  where instrumentid=:id"
                valdict = {'b':bid[0], 'v':bid[1], 'id':row[0]}
                self.__cursor.execute(sqlstr, valdict)
                self.__db.commit() 
            for ask in asks:
                a=n+1
                sqlstr = "update depthmarketdata set bidprice"+str(a)+"=:a, bidvolume"+str(a)+"=:v  where instrumentid=:id"
                valdict = {'a':ask[0], 'v':ask[1], 'id':row[0]}
                self.__cursor.execute(sqlstr, valdict)
                self.__db.commit() 
                n=a
            i+=1
        
        
    def SelectMarketData(self):
        self.UpdateMarketData()
        self.__cursor.execute ("select * from marketdata")
        md = self.__cursor.fetchall()
        if md is None:
            return 'no data'
        else:
            return md 
        
        
    def SelectDepthMarketData(self):
        self.UpdateDepthMarketData()
        self.__cursor.execute ("select * from depthmarketdata")
        md = self.__cursor.fetchall()
        if md is None:
            return 'no data'
        else:
            return md 

    
if __name__=='__main__':
    #OraDBInsert()
#     db1 = cx_Oracle.connect(connStr) 
    with MarketData() as md:
#         md.UpdateMarketData()
#         print md.SelectMarketData()
        print md.SelectDepthMarketData()
        
        
        