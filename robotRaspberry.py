from rcGamepad import rcGamepad
import RPi.GPIO as GPIO
import math

class robotRaspberry():
#    _directionMatrix = [[( 0.0, -1.0), (-1.0,  1.0), (0.0, 1.0)],
#        	        [( 1.0,  1.0), ( 0.0,  0.0), (-1.0, -1.0)],
#	                [(-1.0,  0.0), ( 1.0, -1.0), (1.0, 0.0)] ]

    class motor():
        _motorDirection = { 'forward': (0, 1), 'backwards': (1,0) }
        def __init__( self, pinConfig, pwm_freq ):
            self._pinConfig = pinConfig
            self._pwm_freq = pwm_freq
	    self._motor = self._setupMotorPins()
	

        def _setupMotorPins( self ):
            GPIO.setup( self._pinConfig["dir_A"], GPIO.OUT )
            GPIO.setup( self._pinConfig["dir_B"], GPIO.OUT )
            GPIO.setup( self._pinConfig["pwm"], GPIO.OUT )
            return GPIO.PWM( self._pinConfig["pwm"], self._pwm_freq )

        def setMotorSpeed( self, speed ):
            if speed > 0:
	        self._setDirectionPins( self._motorDirection['forward'] )
	        self._motor.start( speed )
	    else:
	        self._setDirectionPins( self._motorDirection['backwards'] )
	        self._motor.start( -1*speed )

	def _setDirectionPins( self, dPins ):
            GPIO.output( self._pinConfig["dir_A"], dPins[0] )
            GPIO.output( self._pinConfig["dir_B"], dPins[1] )


    def __init__( self, pinConfig, motorConfig ):
        # set the pin numbering scheme
        GPIO.setmode(GPIO.BCM)

        # set pin for output
        self._motorConfig = motorConfig

    	self._motorA = self.motor( pinConfig['motorA'], motorConfig['freq'] )
    	self._motorB = self.motor( pinConfig['motorB'], motorConfig['freq'] )

        self._speed = 0
        self._turnSpeed = (0,0)

    def setSpeed( self, speed ):
        ''' "speed" is actually the pwm duty cycle
        '''
        self._speed = speed
        self._updateSpeed()

    def _updateSpeed( self ):
	print "update speed"
	print "- motor A: base %0.1f, turn %0.1f"%( self._speed, self._turnSpeed[0] )
	print "- motor B: base %0.1f, turn %0.1f"%( self._speed, self._turnSpeed[1] )

	self._motorA.setMotorSpeed( self._speed + self._turnSpeed[0] )
	self._motorB.setMotorSpeed( self._speed + self._turnSpeed[1] )
	return
	
    def setDirection( self, turnSpeed ):
        self._turnSpeed = (turnSpeed, -1*turnSpeed)
        self._updateSpeed()


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
    gp = rcGamepad( robot, speed=70, turnSpeed=30 )
    gp.printJoystickInfo()
    gp.runLoop()
