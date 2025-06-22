from naoqi import ALProxy
import time
from standUp import standUp
from say import say
from speechRecognition import speechRecognition
from moveTo import moveTo
from switchCase import switchCase
from playSoundFile import playSoundFile
from getFile import getFile

# IP del robot NAO 
ROBOT_IP = "192.168.1.100"
PORT = 9559

tts = ALProxy("ALTextToSpeech", ROBOT_IP, PORT)
motion = ALProxy("ALMotion", ROBOT_IP, PORT)
posture = ALProxy("ALRobotPosture", ROBOT_IP, PORT)

# empieza el robot
motion.wakeUp()

posture.goToPosture("StandInit", 0.5)
standUp("StandInit", 0.5)

sentence = "\RSPD="+ str( self.getParameter("Speed (%)") ) + "\ "
sentence += "\VCT="+ str( self.getParameter("Voice shaping (%)") ) + "\ "
sentence += self.getParameter("Hello, whats up. Lets have fun")
sentence +=  "\RST\ "
say(sentence, ROBOT_IP, PORT)

moveTo(0.5, 20, 0.0, ROBOT_IP, PORT)

answer = speechRecognition(ROBOT_IP, PORT)
switchCase(answer, ROBOT_IP, PORT)

if answer == "yes":
    playSoundFile("14-Let_s-Groove.ogg", ROBOT_IP, PORT)
    disco(ROBOT_IP, PORT)
elif answer == "no":
    say("Then, Imma play an instrument", ROBOT_IP, PORT)
    playSoundFile("epicsax.ogg", ROBOT_IP, PORT)
    saxophone(ROBOT_IP, PORT)

    playSoundFile("SONIDO-DE-GUITARRA-ELECTRICA.ogg", ROBOT_IP, PORT)
    guitar(ROBOT_IP, PORT)

# final
motion.rest()
