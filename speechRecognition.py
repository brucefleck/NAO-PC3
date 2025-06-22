class MyClass(GClass):
    def __init__(self):
        GClass.__init__(self, False)

    def onLoad(self):
        try:
            self.asr = self.session().service("ALSpeechRecognition")
        except Exception as e:
            self.asr = None
            self.logger.error(e)
        self.memory = self.session().service("ALMemory")
        from threading import Lock
        self.bIsRunning = False
        self.mutex = Lock()
        self.hasPushed = False
        self.hasSubscribed = False
        self.BIND_PYTHON(self.getName(), "onWordRecognized")

    def onUnload(self):
        from threading import Lock
        self.mutex.acquire()
        try:
            if (self.bIsRunning):
                if (self.hasSubscribed):
                    self.memory.unsubscribeToEvent("WordRecognized", self.getName())
                if (self.hasPushed and self.asr):
                    self.asr.popContexts()
        except RuntimeError, e:
            self.mutex.release()
            raise e
        self.bIsRunning = False;
        self.mutex.release()

    def onInput_onStart(self):
        from threading import Lock
        self.mutex.acquire()
        if(self.bIsRunning):
            self.mutex.release()
            return
        self.bIsRunning = True
        try:
            if self.asr:
                self.asr.pushContexts()
            self.hasPushed = True
            if self.asr:
                self.asr.setVocabulary( self.getParameter("Word list").split(';'), self.getParameter("Enable word spotting") )
            self.memory.subscribeToEvent("WordRecognized", self.getName(), "onWordRecognized")
            self.hasSubscribed = True
        except RuntimeError, e:
            self.mutex.release()
            self.onUnload()
            raise e
        self.mutex.release()

    def onInput_onStop(self):
        if( self.bIsRunning ):
            self.onUnload()
            self.onStopped()

    def onWordRecognized(self, key, value, message):
        if(len(value) > 1 and value[1] >= self.getParameter("Confidence threshold (%)")/100.):
            self.wordRecognized(value[0])
        else:
            self.onNothing()
