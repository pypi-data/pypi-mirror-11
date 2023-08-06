'''
An RMI framework for synapse.
'''
import threading
import traceback

import synapse.link as s_link

from synapse.common import *
from synapse.eventbus import EventBus

class TeleMixin:
    '''
    Telepath RMI Daemon Mixin

    Example:

        import synapse.link as s_link
        import synapse.daemon as s_daemon

        daemon = s_daemon.Daemon()

        class Foo:
            def bar(self, x, y):
                return x + y

        link = s_link.chopLinkUrl('tcp://0.0.0.0:9999')

        daemon.runLinkServer(link)
        daemon.addSharedObject('foo',Foo())

    '''
    def __init__(self): #, statefd=None):

        self.shared = {}

        self.setMesgMethod('tele:syn', self._onMesgTeleSyn )
        self.setMesgMethod('tele:call', self._onMesgTeleCall )

    def addSharedObject(self, name, obj):
        '''
        Share an object via the telepath Server.

        Example:

            foo = Foo()

            serv.addSharedObject('foo',foo)

        '''
        self.shared[name] = obj

    def delSharedObject(self, name):
        '''
        Remove a shared object from the telepath Server.

        Example:

            serv.delSharedObject('foo')

        '''
        return self.shared.pop(name,None)

    def getSharedObject(self, name):
        '''
        Return a reference to a shared object by name.

        Example:

            foo = serv.getSharedObject('foo')

        '''
        return self.shared.get(name)

    def _onMesgTeleSyn(self, sock, mesg):
        '''
        Handle an initial "syn" message from a newly connected client.

        cli: ('syn',{'name':'objname'})
        srv: ('syn',{'meths':[name1, name2, ...],})

        '''
        sock.setSockInfo('tele:syn',True)
        authinfo = mesg[1].get('authinfo')
        ident = self.getAuthIdent(authinfo)
        sock.setSockInfo('tele:ident',ident)
        return tufo('tele:syn')

    def _onMesgTeleCall(self, sock, mesg):

        if not sock.getSockInfo('tele:syn'):
            sock.senderr('nosyn','no syn mesg received')
            return

        _,msginfo = mesg

        oname,mname,args,kwargs = mesg[1].get('teletask')

        if self.authmod != None:
            rule = 'tele.call.%s.%s' % (oname,mname)
            ident = sock.getSockInfo('tele:ident')
            if not self.getAuthAllow(ident,rule):
                sock.senderr('noperm','permission denied')
                return

        obj = self.shared.get(oname)
        if obj == None:
            return tufo('err',code='noobj')

        meth = getattr(obj,mname,None)
        if meth == None:
            return tufo('err',code='nometh')

        try:
            return tufo('tele:call', ret=meth(*args,**kwargs) )

        except Exception as e:
            trace = traceback.format_exc()
            return tufo('tele:call',exc=str(e),trace=trace)

class TeleProtoError(Exception):pass
class TelePermDenied(Exception):pass
class RemoteException(Exception):pass

class ProxyMeth:

    def __init__(self, proxy, name):
        self.name = name
        self.proxy = proxy

    def __call__(self, *args, **kwargs):
        task = (self.proxy.objname, self.name, args, kwargs)

        client = self.proxy._get_client()
        reply = client.sendAndRecv('tele:call',teletask=task)

        if reply[0] == 'tele:call':
            exc = reply[1].get('exc')
            if exc != None:
                raise RemoteException(exc)

            return reply[1].get('ret')

        if reply[1].get('code') == 'noperm':
            raise TelePermDenied()

        raise TeleProtoError( reply[1].get('msg') )
            
class Proxy(EventBus):

    def __init__(self, link):
        EventBus.__init__(self)

        self.link = link
        self.relay = s_link.initLinkRelay(link)
        self.client = self._init_client()

        self._tele_with = {}    # tid:client for with blocks

        # objname is path minus leading "/"
        self.objname = link[1].get('path')[1:]

    def _init_client(self):
        client = self.relay.initLinkClient()
        authinfo = self.link[1].get('authinfo')
        client.sendAndRecv('tele:syn', authinfo=authinfo)
        self.onfini( client.fini, weak=True )
        return client

    def __enter__(self):
        thrid = threading.currentThread().ident
        client = self._init_client()
        self._tele_with[thrid] = client

    def __exit__(self, exc, cls, tb):
        thrid = threading.currentThread().ident
        client = self._tele_with.pop(thrid,None)
        if client != None:
            client.fini()

    def _get_client(self):
        # If the thread is managing a with block, give him his client
        thrid = threading.currentThread().ident
        client = self._tele_with.get(thrid)
        if client != None:
            return client

        return self.client

    def __getattr__(self, name):
        meth = ProxyMeth(self, name)
        setattr(self,name,meth)
        return meth

def getProxy(url):
    '''
    Construct a telepath proxy from a url.

    Example:

        foo = getProxy('tcp://1.2.3.4:90/foo')

        foo.dostuff(30) # call remote method

    '''
    link = s_link.chopLinkUrl(url)
    return Proxy(link)
