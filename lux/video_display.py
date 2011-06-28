"""
An OpenGL based QWidget for displaying the Fiat Lux laser simulator.
"""

from PyQt4 import QtCore, QtGui, QtOpenGL
# custom importer for ARB functions
from OpenGL import GL

from settings import LuxSettings

import math
import numpy
import Queue
import time
import sys
import os

class DisplayError(Exception):
    pass

class VideoDisplay(QtOpenGL.QGLWidget):

    def __init__(self, video_engine, parent=None):

        # Set up to sync with double-buffer, vertical refresh.  Add Alpha and Depth buffers.
        fmt = QtOpenGL.QGLFormat()
        fmt.setSwapInterval(2)
        fmt.setDoubleBuffer(True)
        fmt.setAlpha(True)
        fmt.setDepth(True)
        QtOpenGL.QGLWidget.__init__(self, fmt, parent)

        # set application settings
        self.settings = LuxSettings()

        # create a mutex for the state
        self.lock = QtCore.QMutex()

        # height and width of viewport
        self.width = 512
        self.height = 512

        # set dirty state
        self.dirty = True

        # start up an update timer
        self.timerId = self.startTimer(30)
        
        # whether GL is initialized
        self.initialized = False

        # Start the simulator audio client.  Connects to JACK server,
        # which must be running.
        self.makeCurrent()
        self.video_engine = video_engine
        
    def timerEvent(self, event):
        '''
        Call the OpenGL update function if necessary
        '''
        self.lock.lock()
        dirty = self.dirty
        self.dirty = False
        self.lock.unlock()
        if dirty:
            self.updateGL()

    def setTimerInterval(self, rate):
        '''
        A slot to set a new timer interval corresponding to rate Hz
        '''
        newInterval = int(1000.0/rate+0.5)
        self.lock.lock()
        self.timerInterval = newInterval
        self.killTimer(self.timerId)
        self.timerId = self.startTimer()
        self.lock.unlock()

    def initializeGL(self):
        """Initialize the GL environment we want"""
        self.makeCurrent()

        # Pass the resize_gl call along to the C++ code
        self.video_engine.initialize_gl()

    def resizeGL(self, width=None, height=None):
        '''
        Called when widget is resized
        '''
        self.makeCurrent()

        # Pass the resize_gl call along to the C++ code
        self.video_engine.resize_gl(width, height)

    def paintGL(self):
        """Paint the screen"""
        self.makeCurrent()

        # Call out to the C++ code to do actual, efficient drawing
        self.video_engine.draw_gl()
        self.dirty = True


