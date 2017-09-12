#!/usr/bin/python

# this code is from the official pygame docs
# http://www.pygame.org/docs/ref/joystick.html
# is has been slightly modified from python3 to python2

import pygame
from rc8 import mockRobot

class rcGamepad():
    def __init__( self, robot, speed = 50, turnSpeed = 25, gamepadNo = 0 ):
        self._buttonHandlers = (
            self._doNothing, self._doNothing,
            self._doNothing, self._doNothing,
            self._doNothing, self._doNothing,
            self._doNothing, self._doNothing,
            self._doNothing, self._doQuitButton )

        pygame.joystick.init()

        print "Number of joysticks:", pygame.joystick.get_count()

        self._gpNo = gamepadNo;
        self._initJoystick( self._gpNo )
        self._robot = robot
        self._speed = speed
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
        axisUpDown = 0
        axisLeftRight = 1

        # print self._joystick.get_axis( axisLeftRight )
        # print self._joystick.get_axis( axisUpDown )

        self._robot.setSpeed( self._joystick.get_axis( axisUpDown ) * self._speed )
        self._robot.setDirection( self._joystick.get_axis( axisLeftRight ) * self._turnSpeed )
        # self._robot.updateDirection(  self._joystick.get_axis( axisUpDown ),
        #                               self._joystick.get_axis( axisLeftRight ) )

    def _doQuitButton( self, event ):
        if event.type == pygame.JOYBUTTONUP:
            self._endLoop = True
            print "Quit button - shutting down"

    def _doNothing( self, event ):
        print "Button %d %s - unused"%(event.button, "up" if event.type == pygame.JOYBUTTONUP else "down")
        return

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
