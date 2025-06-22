import time

class MyClass(GClass):
    def __init__(self):
        GClass.__init__(self, False)

    def onLoad(self):
        self.player = self.session().service('ALAudioPlayer')
        self.playerStop = self.session().service('ALAudioPlayer') 
        self.bIsRunning = False
        self.ids = []

    def onUnload(self):
        for id in self.ids:
            try:
                self.playerStop.stop(id)
            except:
                pass
        while( self.bIsRunning ):
            time.sleep( 0.2 )

    def onInput_onStart(self, p):
        self.bIsRunning = True
        try:
            if (self.getParameter("Play in loop")) :
               id = self.player.pCall("playFileInLoop",p,self.getParameter("Volume (%)")/100.,self.getParameter("Balance L/R"))
            else :
               id = self.player.pCall("playFileFromPosition",p,self.getParameter("Begin position (s)"),self.getParameter("Volume (%)")/100.,self.getParameter("Balance L/R"))
            self.ids.append(id)
            self.player.wait(id)
        finally:
            try:
                self.ids.remove(id)
            except:
                pass
            if( self.ids == [] ):
                self.onStopped()
                self.bIsRunning = False

    def onInput_onStop(self):
        self.onUnload()
