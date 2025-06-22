class MyClass(GClass):
    def __init__(self):
        GClass.__init__(self, False)

    def onLoad(self):
        self.nTries = 0
        self.postureService = self.session().service("ALRobotPosture")
        pass

    def onUnload(self):
        self.postureService.stopMove()

    def onInput_onStart(self):
        if(self.nTries != self.getParameter("Maximum of tries")):
            self.nTries = self.getParameter("Maximum of tries")
            self.postureService.setMaxTryNumber(self.nTries)

        result = self.postureService.goToPosture(self.getParameter("Name"), self.getParameter("Speed (%)")/100.)
        if(result):
            self.success()
        else:
            self.failure()
        pass

    def onInput_onStop(self):
        self.onUnload()
        pass
