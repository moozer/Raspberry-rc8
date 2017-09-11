from rcGamepad import rcGamepad
import RPi.GPIO as GPIO
import math

class robotRaspberry():
    _directionMatrix = [[( 0.0, -1.0), (-1.0,  1.0), (0.0, 1.0)],
        	        [( 1.0,  1.0), ( 0.0,  0.0), (-1.0, -1.0)],
	                [(-1.0,  0.0), ( 1.0, -1.0), (1.0, 0.0)] ]


    def __init__( self, pinConfig, motorConfig ):
        # set the pin numbering scheme
        GPIO.setmode(GPIO.BCM)

        # set pin for output
        self._motorConfig = motorConfig
        self._pinConfigA = pinConfig["motorA"]
        self._pinConfigB = pinConfig["motorB"]

    	self._motorA = self._setupMotorPins( self._pinConfigA )
    	self._motorB = self._setupMotorPins( self._pinConfigB )

        self._speed = 0
        self._turnSpeed = (0,0)

    def _setupMotorPins( self, config ):
        GPIO.setup( config["dir_A"], GPIO.OUT )
        GPIO.setup( config["dir_B"], GPIO.OUT )
        GPIO.setup( config["pwm"], GPIO.OUT )
        return GPIO.PWM( config["pwm"], self._motorConfig["freq"] )

    def setSpeed( self, speed ):
        ''' "speed" is actually the pwm duty cycle
        '''
        self._speed = speed
        self._updateSpeed()

    def _updateSpeed( self ):
	print "update speed"
	print "- motor A: base %0.1f, turn %0.1f"%( self._speed, self._turnSpeed[0] )
	print "- motor B: base %0.1f, turn %0.1f"%( self._speed, self._turnSpeed[1] )

        self._motorA.start( self._speed + self._turnSpeed[0] )
        self._motorB.start( self._speed + self._turnSpeed[1] )
        return

    def setDirection( self, turnSpeed ):
        self._turnSpeed = (turnSpeed, -1*turnSpeed)
        self._updateSpeed()


    # def updateDirection( self, x, y ):
    # 	int_x = int( round( x, 0 ) )
    # 	int_y = int( round( y, 0 ) )
    # 	print "input was %f, %f - rounding to %d, %d - (A,B) = %s"%( x, y, int_x, int_y, self._directionMatrix[int_x+1][int_y+1] )
    #     self._setMotorA( self._speed, self._directionMatrix[int_x+1][int_y+1][0] )
    #     self._setMotorB( self._speed, self._directionMatrix[int_x+1][int_y+1][1] )
    #
    def _setMotorA( self, speed, weight ):
        if weight == 0:
            self._motorA.stop()
        else:
            GPIO.output( self._pinConfigA["dir_A"], 0 if weight > 0 else 1 )
            GPIO.output( self._pinConfigA["dir_B"], 1 if weight > 0 else 0 )
            self._motorA.start( speed*math.fabs( weight ) )

    def _setMotorB( self, speed, weight ):
        if weight == 0:
            self._motorB.stop()
        else:
            GPIO.output( self._pinConfigB["dir_A"], 0 if weight > 0 else 1 )
            GPIO.output( self._pinConfigB["dir_B"], 1 if weight > 0 else 0 )
            self._motorB.start( speed*math.fabs( weight ))

    def cleanup( self ):
        self._motorA.stop()
        self._motorB.stop()
        GPIO.cleanup()



if __name__ == "__main__":
    motorConfig = { "freq": 50 }
    pinConfig =   { "motorA": {"dir_A": 14, "dir_B": 15, "pwm": 18 },
                    "motorB": {"dir_A": 3,  "dir_B": 2,  "pwm": 4 }}

    print "using configs"
    print motorConfig
    print pinConfig

    robot = robotRaspberry( pinConfig, motorConfig )
    gp = rcGamepad( robot )
    gp.printJoystickInfo()
    gp.runLoop()
