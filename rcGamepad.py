#!/usr/bin/python

# this code is from the official pygame docs
# http://www.pygame.org/docs/ref/joystick.html
# is has been slightly modified from python3 to python2

import pygame
from rc8 import mockRobot
import time

class rcGamepad():
    def __init__( self, robot, speed = 50, turnSpeed = 25, gamepadNo = 0 ):
        self._buttonHandlers = (
            self._doCircleRight, self._doCircleLeft,
            self._doNothing, self._doNothing,
            self._goFast, self._doNothing,
            self._goSlow, self._doNothing,
            self._doNothing, self._doQuitButton )

        pygame.joystick.init()

        print "Number of joysticks:", pygame.joystick.get_count()

        self._gpNo = gamepadNo;
        self._initJoystick( self._gpNo )
        self._robot = robot
        self._speed = speed
	self._defaultspeed = speed
        self._turnSpeed = turnSpeed

    def _initJoystick( self, gpNo ):
        self._joystick = pygame.joystick.Joystick( gpNo )
        self._joystick.init()

    def getJoystick( self ):
        return self._joystick

    def printJoystickInfo( self ):
        print "- Joystick name:", self._joystick.get_name()
        print "- Number of axes:", self._joystick.get_numaxes()
        print "- Number of buttons:", self._joystick.get_numbuttons()
        print "- Number of hats:", self._joystick.get_numhats()

    def _handleAxis( self, event ):
        axisUpDown = 1
        axisLeftRight = 0

	speed = self._joystick.get_axis( axisUpDown ) * self._speed * -1
	if speed > 100:
		adj_speed = 100
	elif speed < -100:
		adj_speed = -100
	else:
		adj_speed = speed

        self._robot.setSpeed( adj_speed )
        self._robot.setDirection( self._joystick.get_axis( axisLeftRight ) * self._turnSpeed )

    def _doQuitButton( self, event ):
        if event.type == pygame.JOYBUTTONUP:
            self._endLoop = True
            print "Quit button - shutting down"

    def _goSlow( self, event ):
	if event.type == pygame.JOYBUTTONDOWN:
	        print "Button %d %s - go slow"%(event.button, "up" if event.type == pygame.JOYBUTTONUP else "down")
		self._speed = self._defaultspeed/2
	else:
	        print "Button %d %s - go normal"%(event.button, "up" if event.type == pygame.JOYBUTTONUP else "down")
		self._speed = self._defaultspeed
	
    def _goFast( self, event ):
	if event.type == pygame.JOYBUTTONDOWN:
	        print "Button %d %s - go fast"%(event.button, "up" if event.type == pygame.JOYBUTTONUP else "down")
		self._speed = int(self._defaultspeed*1.5)
	else:
	        print "Button %d %s - go normal"%(event.button, "up" if event.type == pygame.JOYBUTTONUP else "down")
		self._speed = self._defaultspeed
	

    def _doNothing( self, event ):
        print "Button %d %s - unused"%(event.button, "up" if event.type == pygame.JOYBUTTONUP else "down")
        return

    def _doCircleRight( self, event ):
        print "Button %d %s - doing circle right"%(event.button, "up" if event.type == pygame.JOYBUTTONUP else "down")
	if event.type == pygame.JOYBUTTONDOWN:
	        self._robot.setSpeed( 0 )
        	self._robot.setDirection( 40 )
		time.sleep( 1.0 )
	        self._robot.setSpeed( 0 )
        	self._robot.setDirection( 0 )
	else:
		print "- button up - doing nothing"

    def _doCircleLeft( self, event ):
        print "Button %d %s - doing circle right"%(event.button, "up" if event.type == pygame.JOYBUTTONUP else "down")
	if event.type == pygame.JOYBUTTONDOWN:
	        self._robot.setSpeed( 0 )
        	self._robot.setDirection( -40 )
		time.sleep( 1.0 )
	        self._robot.setSpeed( 0 )
        	self._robot.setDirection( 0 )
	else:
		print "- button up - doing nothing"

    def _handleButtons( self, event ):
        self._buttonHandlers[event.button](event)

    def _processEvents( self ):
        # EVENT PROCESSING STEP
        for event in pygame.event.get(): # User did something
            if event.joy != self._gpNo:
                continue

            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop

            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                self._handleButtons( event )

            if event.type == pygame.JOYAXISMOTION:
                self._handleAxis( event )

    def runLoop( self ):
        pygame.init()

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        self._endLoop = False

        # -------- Main Program Loop -----------
        while not self._endLoop:
            self._processEvents()

            # Limit to 20 frames per second
            clock.tick(20)

        pygame.quit ()


if __name__ == "__main__":
    robot = mockRobot()
    rcG = rcGamepad( robot )
    rcG.printJoystickInfo()
    rcG.runLoop()
