import time
import msgpack
import collections

import Crypto.Hash.SHA256 as SHA256
import Crypto.PublicKey.RSA as RSA
import Crypto.Signature.PKCS1_v1_5 as PKCS15

import synapse.async as s_async
import synapse.cortex as s_cortex
import synapse.socket as s_socket
import synapse.daemon as s_daemon
import synapse.dyndeps as s_dyndeps
import synapse.threads as s_threads
import synapse.eventbus as s_eventbus

from synapse.statemach import keepstate

from synapse.common import *

class NeuError(Exception):pass
class NoSuchPeer(NeuError):pass

#NOTE: this is still a work in progress, but will be the basis
#      for the new cluster architecture.

class Daemon(s_daemon.Daemon):
    '''
    A Neuron facilitates distributed "mesh" computing through peer routing.

    Each Neuron in a mesh tracks routes and link status messages announced
    by the other neurons and keeps a complete map of the links between each.
    '''

    def __init__(self, statefd=None):

        self.sched      = s_threads.Sched()
        self.asyncpool = s_async.AsyncBoss()

        self.peerbus = s_eventbus.EventBus()

        self.peersocks = {}     # sockets directly connected to peers
        self.peergraph = collections.defaultdict(set)
        self.routecache = {}

        # persistant data in these...
        self.neuinfo = {
            'poolsize':10,  # default to 10 neuron threads
        }
        self.neucores = {}
        self.neusocks = {}  # <guid> : NeuSock()
        self.neushares = {}

        self.runinfo = collections.defaultdict(dict)
        self.peerinfo = collections.defaultdict(dict)

        self.metacore = s_cortex.MetaCortex()

        s_daemon.Daemon.__init__(self)

        self.onfini( self.sched.fini )
        self.onfini( self.peerbus.fini )
        self.onfini( self.asyncpool.fini )

        self.on('link:sock:init',self._onNeuSockInit)

        self.on('neu:peer:init',self._onNeuPeerInit)
        self.on('neu:peer:fini',self._onNeuPeerFini)

        # application layer peer messages...
        self.peerbus.on('ping',self._onPeerBusPing)
        self.peerbus.on('pong',self._onPeerBusPong)

        self.setMesgMethod('neu:data',self._onMesgNeuData)

        self.setMesgMethod('neu:link:syn',self._onMesgNeuLinkSyn)
        self.setMesgMethod('neu:link:synack',self._onMesgNeuLinkSynAck)
        self.setMesgMethod('neu:link:ack',self._onMesgNeuLinkAck)

        self.setMesgMethod('neu:peer:link:up', self._onMesgNeuPeerLinkUp)
        self.setMesgMethod('neu:peer:link:down', self._onMesgNeuPeerLinkDown)

        def setrsakey(event):
            valu = event[1].get('valu')
            self.rsakey = RSA.importKey( valu )
            self.pubkey = self.rsakey.publickey()
            self.pkcs15 = PKCS15.PKCS115_SigScheme( self.rsakey )

        def setauthmod(event):
            valu = event[1].get('valu')
            if valu == None:
                self.setAuthModule(None)
                return

            name,args,kwargs = valu

            auth = s_dyndeps.getDynLocal(name)(*args,**kwargs)
            self.setAuthModule( auth )

        def setpoolsize(event):
            valu = event[1].get('valu')
            self.asyncpool.setPoolSize(valu)

        self.on('neu:info:rsakey', setrsakey)
        self.on('neu:info:authmod', setauthmod)
        self.on('neu:info:poolsize',setpoolsize)

        if statefd:
            self.loadStateFd(statefd)

        #self._loadNeuAuthModule()
        self._loadNeuMetaCortex()
        #self._loadNeuSharedObjects()

        # check if we're brand new...
        if self.neuinfo.get('ident') == None:
            # making a shiney new neuron!
            self.setNeuInfo('ident', guid())

        self.ident = self.getNeuInfo('ident')

        poolsize = self.getNeuInfo('poolsize')
        self.asyncpool.setPoolSize(poolsize)

    def addNeuCortex(self, name, url, tags=()):
        '''
        Add a "persistent" cortex to the neuron.

        Example:

            neu.addNeuCortex('woot.0','ram:///',tags='hehe,haha')

        '''
        core = self.metacore.addCortex(name, url, tags=tags)
        self.addSharedObject('cortex/%s' % (name,), core)
        self._addNeuCortex(name,url,tags=tags)

    def delNeuCortex(self, name):
        '''
        Remove a persistent cortex from the neuron.

        Example:

            neu.delNeuCortex('woot.0')

        Notes:

            * FIXME this takes a restart to take effect

        '''
        self._delNeuCortex(name)

    def addNeuShare(self, path, name, args, kwargs):
        '''
        Add a persistent shared object to the neuron.

        Example:

            neu.addNeuShare

        '''
        self._loadNeuShare(path,name,args,kwargs)
        self._addNeuShare(path,name,args,kwargs)

    def delNeuShare(self, path):
        '''
        Remove a persistent shared object from the neuron.

        Example:

            neu.delNeuShare('foo')

        '''
        self.delSharedObject(path)
        return self._delNeuShare(path)

    def _loadNeuMetaCortex(self):
        for name,url,tags in self.neucores.values():
            self.metacore.addCortex(name,url,tags=tags)

    def _loadNeuShares(self):
        for path,name,args,kwargs in self.neushares.values():
            try:
                self._loadNeuShare(path,name,args,kwargs)
            except Exception as e:
                print('warning (loading share %s): %s' % (path,e))

    def _loadNeuShare(self, path, name, args, kwargs):
        func = s_dyndeps.getDynLocal(name)
        if func == None:
            raise Exception('No Such Func: %s' % (name,))

        self.addSharedObject( path, func(*args,**kwargs) )

    @keepstate
    def _addNeuCortex(self, name, url, tags=None):
        self.neucores[name] = (name,url,tags)

    @keepstate
    def _delNeuCortex(self, name):
        self.neucores.pop(name,None)

    @keepstate
    def _addNeuShare(self, path, name, args, kwargs):
        self.neushares[path] = (path,name,args,kwargs)

    @keepstate
    def _delNeuShare(self, path):
        self.neushares.pop(path,None)

    def genRsaKey(self, bits=2048):
        '''
        Generate a new RSA keypair for the Daemon.
        '''
        rsakey = RSA.generate(bits)
        self.setNeuInfo('rsakey',rsakey.exportKey())
        return rsakey

    def genPeerCert(self,**certinfo):
        '''
        Generate a new peer cert for the Daemon.
        '''
        csr = self.getRsaCertCsr(**certinfo)
        peercert = (csr,())
        peercert = self.signPeerCert(peercert)
        self.setNeuInfo('peercert',peercert)
        return peercert

    def _onPeerBusPing(self, event):
        sent = event[1].get('time')
        self.firePeerResp(event,'pong',time=sent)

    def _onPeerBusPong(self, event):
        jobid = event[1].get('peer:job')

        sent = event[1].get('time')
        rtt = time.time() - sent

        job = self.asyncpool.getAsyncJob(jobid)
        if job == None:
            return

        job.done(rtt)

    def getRsaCertCsr(self, **certinfo):
        '''
        Returns a byte buffer of serialized "cert info" to sign.
        '''
        certinfo['ident'] = self.ident
        certinfo['rsakey'] = self.pubkey.exportKey('DER')
        return msgpack.dumps(certinfo,use_bin_type=True)

    def getPeerPkcs(self, peerid):
        '''
        Return a pkcs15 object for the given peer's cert.

        Example:

            pkcs = neu.getPeerPkcs(peerid)
            if not pkcs.verify(byts,sign):
                return
        '''
        pkcs = self.runinfo[peerid].get('pkcs15')
        if pkcs == None:
            key = self.getPeerInfo(peerid,'rsakey')
            rsa = RSA.importKey( key )
            pkcs = PKCS15.PKCS115_SigScheme(rsa)
            self.runinfo[peerid]['pkcs15'] = pkcs
        return pkcs

    def setNeuInfo(self, prop, valu):
        '''
        Set a property of this Neuron.

        Example:

            neu.setNeuInfo('foo',30)

        '''
        if self.neuinfo.get(prop) == valu:
            return
        self._setNeuInfo(prop, valu)

    @keepstate
    def _setNeuInfo(self, prop, valu):
        self.neuinfo[prop] = valu
        self.fire('neu:info:%s' % prop, valu=valu)

    def getNeuInfo(self, prop):
        '''
        Get a property of this Neuron.

        Example:

            neu.getNeuInfo('foo')

        '''
        return self.neuinfo.get(prop)

    def signWithRsa(self, byts):
        bytehash = SHA256.new(byts)
        return self.pkcs15.sign(bytehash)

    def veriWithRsa(self, byts, sign):
        bytehash = SHA256.new(byts)
        return self.pkcs15.verify(bytehash,sign)

    def syncPingPeer(self, peerid, timeout=6):
        '''
        Synchronously ping a peer by id.

        Example:

            rtt = neu.syncPingPeer(peerid)
            if rtt == None:
                print('timeout!')

        '''
        job = self.jobPingPeer(peerid,timeout=timeout)
        return job.sync(timeout=timeout)

    def jobPingPeer(self, peerid, timeout=6):
        return self.firePeerMesg(peerid,'ping',time=time.time())

    def _onNeuSockInit(self, event):
        '''
        Check if the new sock is from a "peersyn" link.
        '''
        sock = event[1].get('sock')
        # shall we start a peer handshake?
        if sock.getSockInfo('peer'):
            self._sendLinkSyn(sock)

    def _sendLinkSyn(self, sock):
        sock.setSockInfo('neu:link:state','neu:link:syn')
        syninfo = self._getSynInfo()
        sock.fireobj('neu:link:syn',**syninfo)
        sock.setSockInfo('challenge',syninfo['challenge'])

    def _onMesgNeuLinkSyn(self, sock, mesg):
        '''
        neu:link:state - 

            # negotiation states
            neu:link:syn        ( syn sent )
            neu:link:synack     ( synack sent )
            neu:link:ack        ( ack sent )

            # error states
            neu:link:err        ( proto error, must re connect )

            # success states
            neu:link:peer       ( the sock is connected to a peer )
            neu:link:client 

        '''
        if sock.getSockInfo('neu:link:state') != None:
            sock.setSockInfo('neu:link:state','neu:link:err')
            return tufo('neu:link:err',code='badstate')

        ident = mesg[1].get('ident')
        hiscert = mesg[1].get('peercert')
        hischal = mesg[1].get('challenge')

        # possibly accept his cert and add him as a peer
        if hiscert != None:
            self.loadPeerCert(hiscert)

        hiskey = self.getPeerInfo(ident,'rsakey')
        if hiskey == None:
            sock.setSockInfo('neu:link:state','neu:link:err')
            return tufo('neu:link:err',code='nopeerkey')

        chalhash = SHA256.new(hischal)
        chalresp = self.pkcs15.sign(chalhash)

        syninfo = self._getSynInfo()
        syninfo['chalresp'] = chalresp
        syninfo['peeredges'] = self._getPeerEdges()

        # state machine entry point...
        sock.setSockInfo('neu:link:state','neu:link:synack')
        sock.setSockInfo('challenge', syninfo['challenge'] )

        return tufo('neu:link:synack',**syninfo)

    def _onMesgNeuLinkSynAck(self, sock, mesg):
        ident = mesg[1].get('ident')
        hiscert = mesg[1].get('peercert')
        chalresp = mesg[1].get('chalresp')
        challenge = mesg[1].get('challenge')

        if sock.getSockInfo('neu:link:state') != 'neu:link:syn':
            sock.setSockInfo('neu:link:state','neu:link:err')
            return tufo('neu:link:err',code='badstate')

        if hiscert != None:
            self.loadPeerCert(hiscert)

        # do we have a key for him?
        hispkcs = self.getPeerPkcs(ident)
        #hiskey = self.getPeerInfo(ident,'rsakey')
        if hispkcs == None:
            sock.setSockInfo('neu:link:state','neu:link:err')
            return tufo('neu:link:err',code='nopeerkey')

        # grab the challenge we sent him
        sockchal = sock.getSockInfo('challenge')
        if sockchal == None:
            sock.setSockInfo('neu:link:state','neu:link:err')
            return tufo('neu:link:err',code='nochal')

        # verify his sig...
        sockhash = SHA256.new(sockchal)
        if not hispkcs.verify(sockhash,chalresp):
            sock.setSockInfo('neu:link:state','neu:link:err')
            return tufo('neu:link:err',code='badresp')

        # yay! he's a peer
        sock.setSockInfo('neu:link:state','neu:link:peer')
        self.fire('neu:peer:init',sock=sock,ident=ident)

        chalhash = SHA256.new(challenge)
        chalresp = self.pkcs15.sign(chalhash)

        peeredges = self._getPeerEdges()

        for p1,p2 in mesg[1].get('peeredges',()):
            self.addPeerGraphEdge(p1,p2)

        return tufo('neu:link:ack',
                    ident=self.ident,
                    chalresp=chalresp,
                    peeredges=peeredges)

    def _onMesgNeuLinkAck(self, sock, mesg):

        if sock.getSockInfo('neu:link:state') != 'neu:link:synack':
            sock.setSockInfo('neu:link:state','neu:link:err')
            return tufo('neu:link:err',code='badstate')

        ident = mesg[1].get('ident')

        sockchal = sock.getSockInfo('challenge')
        if sockchal == None:
            sock.setSockInfo('neu:link:state','neu:link:err')
            return tufo('neu:link:err',code='nochal')

        hispkcs = self.getPeerPkcs(ident)

        chalresp = mesg[1].get('chalresp')
        chalhash = SHA256.new(sockchal)
        if not hispkcs.verify(chalhash,chalresp):
            sock.setSockInfo('neu:link:state','neu:link:err')
            return tufo('neu:link:err',code='badresp')

        for p1,p2 in mesg[1].get('peeredges',()):
            self.addPeerGraphEdge(p1,p2)

        sock.setSockInfo('neu:link:state','neu:link:peer')
        self.fire('neu:peer:init',sock=sock,ident=ident)

    def _onMesgNeuLinkErr(self, sock, mesg):
        sock.setSockState('neu:link:state','neu:link:err')
        sock.fini()

    def addPeerCert(self, peercert):
        '''
        Called *after* validation to absorb cert info.

        Example:

            neu.addPeerCert(peercert)

        '''
        hisinfo,hissigs = peercert
        peerinfo = msgpack.loads(hisinfo,use_list=False,encoding='utf8')

        # lets absorb his cert info!
        ident = peerinfo.get('ident')
        for prop,valu in peerinfo.items():
            # FIXME make an API to check then set
            if self.peerinfo[ident].get(prop) != valu:
                self.setPeerInfo(ident,prop,valu)

    def signPeerCert(self, peercert):
        '''
        Add our signature to a peer cert tuple.
        '''
        byts,signs = peercert
        sign = self.signWithRsa(byts)
        certsign = (self.ident,sign)
        return (byts, peercert[1] + (certsign,))

    def loadPeerCert(self, peercert):
        '''
        Parse/Validate a peer cert and absorb its info if valid.
        '''
        hisinfo,hissigs = peercert

        hishash = SHA256.new(hisinfo)
        verified = False
        for ident,sign in hissigs:

            if not self.isKnownPeer(ident):
                continue

            if not self.getPeerInfo(ident,'signer'):
                continue

            pkcs = self.getPeerPkcs(ident)
            if pkcs == None:
                continue

            if not pkcs.verify(hishash,sign):
                continue

            verified = True
            break

        if not verified:
            return False

        self.addPeerCert(peercert)
        return True

    def _getPeerEdges(self):
        ret = []
        for peer,peers in self.peergraph.items():
            ret.extend([ (peer,p) for p in peers ])
        return ret

    def _getSynInfo(self):
        info = {
            'ident':self.ident,
            'peercert':self.getNeuInfo('peercert'),
            'challenge':guid(),
        }
        return info

    def setPeerInfo(self, peerid, prop, valu):
        '''
        Set a property about a peer.

        Example:

            neu.setPeerInfo(peerid,'foo',30)

        '''
        if self.peerinfo[peerid].get(prop) == valu:
            return

        self._setPeerInfo(peerid, prop, valu)

    @keepstate
    def _setPeerInfo(self, peerid, prop, valu):
        self.peerinfo[peerid][prop] = valu

    def getPeerInfo(self, peerid, prop):
        '''
        Return a property about a peer by id.

        Example:

            neu.getPeerInfo(peerid,'foo')

        '''
        # FIXME what do we do with invalid peerid?
        info = self.peerinfo.get(peerid)
        if info == None:
            raise NoSuchPeer(peerid)
        return info.get(prop)

    def isKnownPeer(self, peerid):
        '''
        Check if we know of a peer with the given id.

        Example:

            if neu.isKnownPeer(peerid):
                stuff()

        '''
        return self.peerinfo.get(peerid) != None

    def _onNeuPeerInit(self, event):
        sock = event[1].get('sock')
        peerid = event[1].get('ident')

        self.peersocks[peerid] = sock
        self.addPeerGraphEdge(self.ident,peerid)

        # Send out a peercast mesg for link up!
        edge = (self.ident,peerid)
        self.firePeerCast('neu:peer:link:up',edge=edge)

    # FIXME implement triggering this
    def _onNeuPeerFini(self, event):
        sock = event[1].get('sock')
        peerid = event[1].get('ident')

        # FIXME remove all graph links with this peer
        # FIXME remove all graph links only reachable via this peer?

        if self.peersocks.get(peerid) == sock:
            # sched an announce of link down
            pass

    def _onMesgNeuPeerLinkUp(self, sock, mesg):
        if sock.getSockInfo('neu:link:state') != 'neu:link:peer':
            return

        edge = mesg[1].get('edge')
        if edge == None:
            return

        peer1,peer2 = edge
        self.addPeerGraphEdge(peer1,peer2)

        # continue routing the message
        self.routePeerCast(mesg)

    def _onMesgNeuPeerLinkDown(self, sock, mesg):
        pass

    def addPeerGraphEdge(self, srcident, dstident):
        '''
        Add a new link between known peers in our peer graph.
        '''
        self.peergraph[srcident].add(dstident)

    def delPeerGraphEdge(self, srcident, dstident):
        '''
        Remove a link between known peers in our peer graph.
        '''
        self.peergraph[srcident].discard(dstident)

    def firePeerCast(self, name, **msginfo):
        '''
        Fire a message to all reachable peers.
        '''

        trees = self._getPeerCast()

        mesg = (name,msginfo)
        for node in trees:

            msginfo['peer:route'] = node

            sock = self.peersocks.get(node[0])
            sock.sendobj(mesg)
            # FIXME handle sock down re-broadcast

    def _sendToPeer(self, peerid, mesg):
        '''
        Route an neu message to a peer.
        '''
        byts = msgpack.dumps(mesg, use_bin_type=True)
        self._sendPeerByts(peerid, byts)

    def _sendPeerByts(self, peerid, byts, **msginfo):

        route = self._getPeerRoute(peerid)
        if route == None:
            print('no route: %s' % (peerid,))
            # FIXME retrans
            return

        nexthop = route[1]

        msginfo['hop'] = 0
        msginfo['mesg'] = byts
        msginfo['route'] = route
        datamesg = ('neu:data',msginfo)

        sock = self.peersocks.get(nexthop)
        if sock == None:
            # FIXME RETRANS
            return

        if not sock.sendobj( datamesg ):
            # FIXME RETRANS
            return

    def _onMesgNeuData(self, sock, mesg):
        '''
        A Neuron "data" message which should be routed.

        ('neu:data', {
            'hop':<int>, # index into route
            'route':[srcpeer, ... ,dstpeer] # neu:data is source routed
            'mesg':<byts>,
        })

        '''
        if sock.getSockInfo('neu:link:state') != 'neu:link:peer':
            # FIXME logging
            print('neu:data from nonpeer: %s' % (sock,))
            return

        hop = mesg[1].get('hop') + 1
        route = mesg[1].get('route')

        # update the hop index.
        mesg[1]['hop'] = hop

        nexthop = route[hop]
        if nexthop == self.ident:
            peermesg = msgpack.loads(mesg[1]['mesg'],use_list=False,encoding='utf8')
            self.peerbus.dist(peermesg)
            return

        fwdsock = self.peersocks.get(nexthop)
        if fwdsock == None:
            return self._schedMesgRetrans(nexthop, mesg)

        if not fwdsock.sendobj(mesg):
            return self._schedMesgRetrans(nexthop, mesg)

    def firePeerMesg(self, peerid, name, **msginfo):
        '''
        Fire an async job wrapped peer message and return the job.
        '''
        job = self.asyncpool.initAsyncJob()

        msginfo['peer:dst'] = peerid
        msginfo['peer:job'] = job.jid
        msginfo['peer:src'] = self.ident

        self._sendToPeer( peerid, (name,msginfo) )
        return job

    def firePeerResp(self, mesg, name, **msginfo):
        '''
        Fire a response "peerbus" message (via neu:data routing).
        '''
        peerid = mesg[1].get('peer:src')
        if peerid == None:
            return

        msginfo['peer:dst'] = peerid
        msginfo['peer:src'] = self.ident
        msginfo['peer:job'] = mesg[1].get('peer:job')

        self._sendToPeer( peerid, (name,msginfo) )

    def routePeerCast(self, mesg):
        '''
        Continue routing a peercast message.

        Notes:

            * This API may modify mesg[1]['peer:route']

        '''
        node = mesg[1].get('peer:route')
        if node == None:
            return

        for nextnode in node[1]:
            mesg[1]['peer:route'] = nextnode
            sock = self.peersocks.get(nextnode[0])
            if sock == None:
                # FIXME handle sock down re-broadcast
                continue

            sock.sendobj(mesg)

    def _getPeerCast(self):
        '''
        Construct a list of "shortest path" trees to each reachable peer.
        '''
        links = self.peersocks.keys()

        done = set(links)
        done.add( self.ident )

        trees = [ (link, []) for link in links ]
        todo = collections.deque( trees )

        while todo:
            node = todo.popleft()

            for n2 in self.peergraph[node[0]]:

                if n2 in done:
                    continue

                done.add(n2)
                nextnode = (n2,[])

                todo.append( nextnode )
                node[1].append( nextnode )

        return trees

    def _getPeerRoute(self, peerid):
        '''
        Calculate and return the shortest known path to peer.
        '''
        route = self.routecache.get(peerid)
        if route != None:
            return route

        done = set()
        todo = collections.deque(( [self.ident,], ))

        # breadth first search...
        while todo:

            route = todo.popleft()
            lasthop = route[-1]

            if lasthop in done:
                continue

            done.add(lasthop)

            for n2 in self.peergraph[lasthop]:

                if n2 == peerid:
                    route.append(n2)
                    self.routecache[peerid] = route
                    return route

                if n2 in done:
                    continue

                todo.append( route + [n2] )
