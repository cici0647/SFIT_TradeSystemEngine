#! /usr/bin/env python
#coding=gbk
'''
Created on 2015-4-20

@author: lu.siqiao
'''
import cx_Oracle
#包括报单的撤销，挂起，激活，修改
import defaultData

class OrderAction:
    def __enter__(self):
        connStr = 'MDB/oracle@192.168.24.108/tradeTester'
        self.__db__ = cx_Oracle.Connection(connStr)
        self.__cursor__ = self.__db__.cursor()
        return self 
  
    def __exit__(self, type, value, traceback): 
        self.__db__.close()
        
    def OrderAction_Delete(self,OrderSysID):
        defaultData.ReqOrderAction_d.update(OrderSysID)
        sqlStr1 = "DELETE FROM T_ORDERBOOKLIST WHERE ORDERSYSID = :b_orderSysID"
        dictOrder1 = {'b_orderSysID': defaultData.ReqOrderAction_d['OrderSysID']}
        self.__cursor__.execute(sqlStr1, dictOrder1)
        self.__db__.commit()
          
    def OrderAction_Suspend(self,OrderStatus):
        try:
            sqlStr = "UPDATE FROM T_ORDERS WHERE ORDERSTATUS = :b_OrderStatus"
            dictOrder = {'b_orderSysID': OrderStatus}
            self.__cursor__.execute(sqlStr, dictOrder)
            self.__db__.commit()
        except Exception, e:
            print e
               
    def OrderAction_Invoke(self,OrderStatus):
        try:
            sqlStr = "UPDATE FROM T_ORDERS WHERE ORDERSTATUS = :b_OrderStatus"
            dictOrder = {'b_orderSysID': OrderStatus}
            self.__cursor__.execute(sqlStr, dictOrder)
            self.__db__.commit()
        except Exception, e:
            print e       
    
if __name__ == '__main__':
    with OrderAction() as orderaction:
        orderaction.OrderAction_Delete()
        
        
    
