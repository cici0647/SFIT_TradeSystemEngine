'''
Created on 2015-4-24

@author: kong.lihua

This module is used to send complex object between sever and client.
'''
from twisted.spread import pb

class Request:
    def __init__(self, name, paraDict):
        self.name = name
        self.paraDict = paraDict
    
class ClientRequest(Request, pb.Copyable):
    pass

class ServerRequest(pb.RemoteCopy, Request):
    pass

pb.setUnjellyableForClass(ClientRequest, ServerRequest)
