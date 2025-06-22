class MyClass(GClass):
    def __init__(self):
        GClass.__init__(self, False)

    def onLoad(self):
        pass

    def onInput_onStart(self):
        self.onStopped(self.behaviorAbsolutePath() + self.getParameter("File name"))
