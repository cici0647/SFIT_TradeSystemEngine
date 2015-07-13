#! /usr/bin/env python
#coding=gbk
'''
Created on 2015-5-28
@author: zhu.jing
'''
import logging
import types

LOGGER = logging.getLogger('tradeEngine') 
LOGPATH = './log/te.log'

#打印日志信息
#LOGGER.setLevel(int(TCconfig.get_tc_ini('setLogLevel')))
LOGGER.setLevel(10)
loghandler_f=logging.FileHandler(LOGPATH)  #from zhou.xq
#loghandler_f.setLevel(int(TCconfig.get_tc_ini('setLogLevel_f')))
loghandler_f.setLevel(10)
loghandler_s=logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#add log to file
loghandler_f.setFormatter(formatter)
#print log to screem
loghandler_s.setFormatter(formatter)
LOGGER.addHandler(loghandler_f)
LOGGER.addHandler(loghandler_s)


def main():  
    LOGGER.warning("error received: first try") 
    LOGGER.info("info received: first try") 
    LOGGER.debug("debug received: first try")  

if __name__ == '__main__':
    main()