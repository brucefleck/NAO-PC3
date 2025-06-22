import time

class MyClass(GClass):
    def __init__(self):
        GClass.__init__(self, False)

    def onLoad(self):
        self.tts = self.session().service('ALTextToSpeech')
        self.ttsStop = self.session().service('ALTextToSpeech')
        self.bIsRunning = False
        self.ids = []

    def onUnload(self):
        for id in self.ids:
            try:
                self.ttsStop.stop(id)
            except:
                pass
        while( self.bIsRunning ):
            time.sleep( 0.2 )

    def onInput_onStart(self):
        self.bIsRunning = True
        try:
            sentence = "\RSPD="+ str( self.getParameter("Speed (%)") ) + "\ "
            sentence += "\VCT="+ str( self.getParameter("Voice shaping (%)") ) + "\ "
            sentence += self.getParameter("Text")
            sentence +=  "\RST\ "
            id = self.tts.pCall("say",str(sentence))
            self.ids.append(id)
            self.tts.wait(id)
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
