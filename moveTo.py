
class MyClass(GClass):
    def __init__(self):
        GClass.__init__(self, False)
        self.positionErrorThresholdPos = 0.01
        self.positionErrorThresholdAng = 0.03

    def onLoad(self):
        self.motion = self.session().service("ALMotion")

    def onUnload(self):
        self.motion.moveToward(0.0, 0.0, 0.0)

    def onInput_onStart(self):
        import almath
        initPosition = almath.Pose2D(self.motion.getRobotPosition(True))
        targetDistance = almath.Pose2D(self.getParameter("Distance X (m)"),
            self.getParameter("Distance Y (m)"),
            self.getParameter("Theta (deg)") * almath.PI / 180)
        expectedEndPosition = initPosition * targetDistance
        enableArms = self.getParameter("Arms movement enabled")
        self.motion.setMoveArmsEnabled(enableArms, enableArms)
        self.motion.moveTo(self.getParameter("Distance X (m)"),
            self.getParameter("Distance Y (m)"),
            self.getParameter("Theta (deg)") * almath.PI / 180)

        realEndPosition = almath.Pose2D(self.motion.getRobotPosition(False))
        positionError = realEndPosition.diff(expectedEndPosition)
        positionError.theta = almath.modulo2PI(positionError.theta)
        if (abs(positionError.x) < self.positionErrorThresholdPos
            and abs(positionError.y) < self.positionErrorThresholdPos
            and abs(positionError.theta) < self.positionErrorThresholdAng):
            self.onArrivedAtDestination()
        else:
            self.onStoppedBeforeArriving(positionError.toVector())

    def onInput_onStop(self):
        self.onUnload()
