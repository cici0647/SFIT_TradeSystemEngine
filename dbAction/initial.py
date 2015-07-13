#/usr/bin/python
#coding=gbk
'''
Created on 2015-5-5

@author: lu.siqiao
'''

from perf import Tinit
import os

if __name__ == '__main__':
    TinitcsvList = os.listdir('./perf')
    for tinitcsv in TinitcsvList:
        if tinitcsv.split('.')[-1] == 'csv':
            Tinit.FilesToDb.fileToDb(tinitcsv)

