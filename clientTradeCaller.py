'''
Created on 2015-4-15
 
@author: kong.lihua
'''
import time
from twisted.internet import reactor
from twisted.spread import pb
from twisted.cred.credentials import UsernamePassword
from reqClazz import ClientRequest


class TradeClientFactory(pb.PBClientFactory):
    
    def __init__(self, caller, connected):
        pb.PBClientFactory.__init__(self)
        self._caller = caller
        self._onConnected = connected
    
    def clientConnectionMade(self, broker):
        pb.PBClientFactory.clientConnectionMade(self, broker)
        self._caller.remote_print({'errorCode': 0, 'msg': 'connect success', 'CallbackFunc': 'OnFrontConnected'})
        self._onConnected()
        
    def clientConnectionLost(self, connector, reason, reconnecting=0):
        pb.PBClientFactory.clientConnectionLost(self, connector, reason, reconnecting=reconnecting)
#to do: display connection lost reason
        self._caller.remote_print({'errorCode': -1, 'msg': 'connect lost', 'CallbackFunc': 'OnFrontDisconnected'})

class TradeCaller(object):
 
    def __init__(self, reqQueue):
        self.client = RtnTrade()
        self.factory = TradeClientFactory(self.client, self.connected)
        reactor.connectTCP("localhost", pb.portno, self.factory)
        #defer = self.factory.login(UsernamePassword("admin", "123"), client=RtnTrade())
        #defer.addCallbacks(self.connected, self.loginFailure)
#added by zhu.j
        #d = self.factory.getRootObject()
        #d.addCallback(self.connected)
        self.reqQueue = reqQueue
     
        reactor.run()
        
    def connected(self):
        self.request(None)
     
    def loginSuccess(self,perspective):
        self.perspective = perspective
         
    def request(self, p):
        req = self.reqQueue.get()
        if req['funcName'] == 'ReqUserLogin':
            user = req['input'].get('userid')
            pwd = req['input'].get('password')
            d = self.factory.login(UsernamePassword(user, pwd), client=self.client).addCallbacks(self.loginSuccess, self.loginFailure)
        elif req['funcName'] == 'ReqUserLogout':
            self.client.remote_print({'CallbackFunc': 'OnRspUserLogout'})
            self.factory.disconnect()
            return
        else:
            d = self.perspective.callRemote("req", req).addCallbacks(self.success, self.failure)
        d.addCallback(self.request)

                
    def success(self, message):
        print "Message received:",message
        #reactor.stop()
 
    def failure(self, error):
#         t = error.trap(DefinedError)
        print "error received:", error.value
        reactor.stop()
        print time.clock()
         
    def loginFailure(self, error):
        from twisted.cred.error import UnauthorizedLogin,LoginFailed,Unauthorized
        t = error.trap(Unauthorized)
        print "error received:", t
        reactor.stop()
 
 
class RtnTrade(pb.Root):
    def remote_print(self, msg):
        print "message return:" , msg

def sessionRun(lock, q):
    tc = TradeCaller(q)
    
def main():   
    import multiprocessing
    #req = ("ReqOrderInsert", {'a':1, 'b':2})
    
#     req = ('ReqOrderInsert', {'ContingentCondition': '1', 'CombOffsetFlag': '0', 'UserID': '0017cac', 'LimitPrice': 16400, 'Direction': '1', 
#                           'ParticipantID': '0017', 'VolumeTotalOriginal': 1, 'SettlementGroupID': '00000001', 'ClientID': '00000017', 'OrderPriceType': '2', 
#                           'TimeCondition': '3', 'OrderSysID': '000000000012', 'IsAutoSuspend': 0, 'StopPrice': 0, 'InstrumentID': 'al1208                        ', 
#                           'MinVolume': 0, 'SettlementID': 1, 'ForceCloseReason': '0', 'TradingDay': '20150423', 'CombHedgeFlag': '1', 
#                           'BusinessLocalID': 0, 'GTDDate': '', 'OrderLocalID': 'smok00000804', 'BusinessUnit': '', 'VolumeCondition': '1'})

    processArr = []
    lock = multiprocessing.Lock()
 
    q = multiprocessing.Queue()

#     process 1
    process1 = multiprocessing.Process(target=sessionRun,args=(lock,q))
    process1.start()
   
    q.put({'funcName':'ReqUserLogin', 'input':{'userid': '0017aca', 'password': '1'}})
#     for i in range(0,10):
#         dict = {'a': "ff", 'b':i}
#         q.put(('ReqOrderInsert', dict))
#     q.put(('ReqUserLogout', dict))
#     
#     q.put(req)
    time.sleep(15)
    reqDict = {'UserID':'0017aca','ClientID':'00000017','ParticipantID':'0017',
                            'InstrumentID':'cu1211','CombOffsetFlag':'0','CombHedgeFlag':'1',
                            'VolumeTotalOriginal':1,'LimitPrice':17000,'Direction':'1',
                            'OrderLocalID':'1001'
                            }
    dict = {'funcName':'ReqOrderInsert','ApiType':'TE','input':reqDict}
    q.put(dict)
    process1.join()
#     reqLogin = ('ReqUserLogin',  {'userid': '0017cac', 'password': '1'})
#     TradeCaller(reqLogin).callServer()   
     
if __name__ == '__main__':
    main() 
