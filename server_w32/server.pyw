import pyHook, wx, os

try:
    from twisted.internet import wxreactor
    wxreactor.install()
except:
    print "falling back to default reactor"
    pass
from twisted.internet import reactor

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol

class BroadcastServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, msg, binary):
        if not binary and msg == 'Ping':
            self.sendMessage('Pong')

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)

class BroadcastServerFactory(WebSocketServerFactory):
 
    protocol = BroadcastServerProtocol

    def __init__(self):
        WebSocketServerFactory.__init__(self)
        self.clients = []

    def register(self, client):
        if not client in self.clients:
            print "registered client " + client.peerstr
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print "unregistered client " + client.peerstr
            self.clients.remove(client)

    def broadcast(self, msg):
        print "broadcasting message '%s' .." % msg
        for c in self.clients:
            print "send to " + c.peerstr
            c.sendMessage(msg)

def appIcon():
    from wx.lib.embeddedimage import PyEmbeddedImage

    return PyEmbeddedImage(
        "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"
        "YII=").getIcon()
            
if __name__ == "__main__":
    factory = BroadcastServerFactory()
    
    def OnTaskBarRight(event):
        app.ExitMainLoop()
        
    keys = {
        'Media_Play_Pause':'16',
        'Media_Prev_Track':'20',
        'Media_Next_Track':'19'}
    
    def callback(event):
        key = event.Key
        if key in keys:
            factory.broadcast(keys[key])
        return True
        
    hm = pyHook.HookManager()
    hm.KeyDown = callback
    hm.HookKeyboard()
    
    app = wx.PySimpleApp()
    tbi = wx.TaskBarIcon()
    tbi.SetIcon(appIcon(), "KeySocket Server (double right click to exit)")
    wx.EVT_TASKBAR_RIGHT_DCLICK(tbi, OnTaskBarRight)    
    reactor.registerWxApp(app)
    
    reactor.listenTCP(1337, factory)
    reactor.run()
    hm.UnhookKeyboard()
