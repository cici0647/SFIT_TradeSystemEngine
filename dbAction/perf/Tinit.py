#/usr/bin/python
#coding=gbk
'''
Created on 2015-5-4

@author: lu.siqiao
'''
#初始化数据导入数据库
import cx_Oracle
import csv 
import xlrd 

class ImportOracle(object): 
    def inoracle(self): 
        pass
  
    def connOracle(self): 
        conn = cx_Oracle.connect('sync/oracle@192.168.24.108/tradeTester') 
        cursor = conn.cursor() 
  
        #fields = [i+' varchar2(200)' for i in self.title] 
        #fields_str = ', '.join(fields) 
        #sql = 'create table %s (%s)' % (self.table_name, fields_str) 
        #print sql 
        #cursor.execute(sql) 
        
        sql = 'Truncate table %s' % (self.table_name) 
        print sql 
        cursor.execute(sql) 
  
        a = [':%s' %i for i in range(len(self.title)+1)] 
        value= ','.join(a[1:]) 
        sql = 'insert into %s values(%s)' %(self.table_name, value) 
        print sql 
  
        cursor.prepare(sql) 
        cursor.executemany(None, self.data) 
  
        cursor.close() 
        conn.commit() 
        conn.close() 

  
class ImportOracleCsv(ImportOracle): 
    def inoracle(self): 
        print self.filename
        with open('./perf/' + self.filename, 'rb') as f: 
            reader = csv.reader(f) 
            contents = [i for i in reader] 
  
        title = contents[0] 
        data = contents[1:] 
  
        return (title, data) 
    
class ImportOracleExcel(ImportOracle): 
    def inoracle(self): 
        wb = xlrd.open_workbook(self.filename) 
        sheet1 = wb.sheet_by_index(0) 
  
        title = sheet1.row_values(0) 
        data = [sheet1.row_values(row) for row in range(1, sheet1.nrows)] 
        return (title, data) 
    
class ImportOracleError(ImportOracle): 
    def inoracle(self): 
        print 'Undefine file type'
        return 0        
  
class ChooseFactory(object): 
    choose = {} 
    choose['csv'] = ImportOracleCsv() 
    choose['xlsx'] = ImportOracleExcel() 
    choose['xls'] = ImportOracleExcel() 
  
    def choosefile(self, ch): 
        if ch in self.choose: 
            op = self.choose[ch] 
        else: 
            op = ImportError() 
  
        return op 
    
class FilesToDb(object):
    @classmethod
    def fileToDb(self,file_name):
        op = file_name.split('.')[-1]
        table_name = file_name.split('.')[0]
        factory = ChooseFactory() 
        cal = factory.choosefile(op) 
        cal.filename = file_name 
        (cal.title, cal.data) = cal.inoracle() 
        cal.table_name = table_name 
        cal.connOracle()
        

 
        
    #def FilesToDb(self,filesname):

        
        
# if __name__ =="__main__": 
#     file_name = 't_MarketData.csv'
#     table_name= 't_MarketData'
#     op = file_name.split('.')[-1] 
#     factory = ChooseFactory() 
#     cal = factory.choosefile(op) 
#     cal.filename = file_name 
#     (cal.title, cal.data) = cal.inoracle() 
#     cal.table_name = table_name 
#     cal.ConnOracle()
        