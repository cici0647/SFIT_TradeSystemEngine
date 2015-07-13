#! /usr/bin/env python
#coding=gbk
'''
@author: zhang.jinxian

modify on 2015-5-28
@author: zhu.jing
增加公有流私有流方法
使用sysLogger功能
'''
from zope.interface import implements
from twisted.spread import pb
from twisted.cred.portal import IRealm
from twisted.internet import reactor
from twisted.cred.portal import Portal
from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse
from tradeEngine import TradeEngine
from reqClazz import ServerRequest
import sysLogger 


if __name__ == '__main__':
    # Avoid using any names defined in the "__main__" module.
    from tradeServer import main
    raise SystemExit(main())

class DefinedError(pb.Error):
    pass

class MyPerspective(pb.Avatar):
    def __init__(self, name):
        self.name = name
        
    def attached(self, mind):
        self.remote = mind
        #self.server.remote = self.remote
        
        self.server.onLogin(self.name)
#         self.server.reqConnect()
    def detached(self, mind):
        self.remote = None
    
    def perspective_req(self, request):  
        #rtns = self.server.handleRequest(request, self.name)
        rtns = getattr(self.server, request['funcName'], None)(request['input'])
        return rtns
        #return request[0] + "_rtns"
    
    def perspective_error(self):
        raise DefinedError("exception!")
    
    def logout(self):
        #print self, "logged out"
        sysLogger.LOGGER.info("logged out")

class TradeRealm:      
    implements(IRealm) 
    def  __init__(self): 
        self.groups = {} # indexed by name
        self.users = {} # indexed by name
        
    def requestAvatar(self, avatarId, mind, *interfaces):
        if pb.IPerspective in interfaces:
            
            username = avatarId
            groupname = username[:4]
            #print 'groupname: ', self.groupname
            self.users[username] = mind 
            print "couple: ", username, ", ", mind
            #print 'user: ', self.users[self.username]            
            if not self.groups.has_key(groupname):
                self.groups[groupname] = []                
            self.groups[groupname].append(username)
            #print 'group: ', self.groups[self.groupname] 
            
            avatar = MyPerspective(avatarId)
            #print 'avatarId: ', avatarId   
            avatar.server = self.server
            avatar.attached(mind)
            return pb.IPerspective, avatar, avatar.logout 
        else:
            raise NotImplementedError("no interface")
    
    def privateSent(self, msg, username):
        #print 'private sent: ', username, self.users[username], msg
        sysLogger.LOGGER.debug("private sent: %s, %s, %s", username, self.users[username], msg)
        self.users[username].callRemote("print", msg)
    
    def groupSent(self, msg, username):
        
        groupname = username[:4]
        group = self.groups[groupname]
        if group:
            #print 'group sent', group
        # send the message to all members of the group
            for user in group:
                #print 'group sent: ', user, self.users[user], msg
                sysLogger.LOGGER.debug("group sent: %s, %s, %s", username, self.users[username], msg)
                self.users[user].callRemote("print", msg)
        
    def publicSent(self, msg):
        # send the message to all members
        for group in self.groups:
            for user in group:
                #print 'user sent: ', user, self.users[user], msg
                sysLogger.LOGGER.debug("public sent: %s, %s, %s", user, self.users[user], msg)
                self.users[user].callRemote("print", msg)

def main():
    realm = TradeRealm()
    realm.server = TradeEngine(realm)
    
    checker = InMemoryUsernamePasswordDatabaseDontUse()
    checker.addUser("guest", "guest")
    checker.addUser("admin","123")
    checker.addUser("0017aca","1")
    checker.addUser('0017cac','1')
    portal = Portal(realm, [checker])  
    
    factory = pb.PBServerFactory(portal)
    reactor.listenTCP(pb.portno, factory)
    reactor.run()
    
