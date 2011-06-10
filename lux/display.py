"""
An OpenGL based QWidget for displaying the Fiat Lux laser simulator.
"""

from PyQt4 import QtCore, QtGui, QtOpenGL
# custom importer for ARB functions
from OpenGL import GL

from xenon_lux import LuxSimulatorAudioClient

import math
import numpy
import Queue
import time
import sys
import os

class DisplayError(Exception):
    pass

class SimulationDisplay(QtOpenGL.QGLWidget):

    def __init__(self, settings, parent=None):

        # Set up to sync with double-buffer, vertical refresh.  Add Alpha and Depth buffers.
        fmt = QtOpenGL.QGLFormat()
        fmt.setSwapInterval(1)
        fmt.setDoubleBuffer(True)
        fmt.setAlpha(True)
        fmt.setDepth(True)
        QtOpenGL.QGLWidget.__init__(self, fmt, parent)

        # the display settings window
        self.displaySettings = None
        
        # set application settings
        self.settings = settings

        # create a mutex for the state
        self.lock = QtCore.QMutex()

        # height and width of viewport
        self.width = 512
        self.height = 512

        # set dirty state
        self.dirty = False

        # start up an update timer
        self.timerId = self.startTimer(30)
        
        # whether GL is initialized
        self.initialized = False

        # Start the simulator audio client.  Connects to JACK server,
        # which must be running.
        self.audio_client = LuxSimulatorAudioClient("lux_simulator");
        self.audio_client.add_input_port("in_x")
        self.audio_client.add_input_port("in_y")
        self.audio_client.add_input_port("in_r")
        self.audio_client.add_input_port("in_g")
        self.audio_client.add_input_port("in_b")
        self.audio_client.add_input_port("in_a")
        self.audio_client.start()

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

	GL.glClearColor(0.0, 0.0, 0.0, 0.0);
	GL.glClearDepth(1.0);
	GL.glDepthFunc(GL.GL_LESS);
	GL.glDisable(GL.GL_DEPTH_TEST);
	GL.glEnable(GL.GL_BLEND);
	GL.glBlendFunc (GL.GL_SRC_ALPHA, GL.GL_ONE);
	GL.glEnable(GL.GL_POINT_SMOOTH);
	GL.glEnable(GL.GL_LINE_SMOOTH);

    def resizeGL(self, width=None, height=None):
        '''
        Called when widget is resized
        '''
        self.makeCurrent()

        # Pass the resize_gl call along to the C++ code
        self.audio_client.resize_gl(width, height)

    def paintGL(self):
        """Paint the screen"""
        self.makeCurrent()

        # Call out to the C++ code to do actual, efficient drawing
        self.audio_client.draw_gl()
        self.dirty = True

class SimulationSettings(QtGui.QWidget):
    """
    A window that has the various display-specific settings
    """
    def __init__(self, displayWindow, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.displayWindow = displayWindow
        self.displayWindow.displaySettings = self

        self.audioOptionsGroup = QtGui.QGroupBox('Audio Settings', self)
        self.audioOptionsLayout = QtGui.QGridLayout(self.audioOptionsGroup)
        self.test1Options = QtGui.QCheckBox('Test1')
        self.test1Options.setVisible(False)
        self.audioOptionsLayout.addWidget(self.test1Options, 0, 0)
        self.audioOptionsGroup.setLayout(self.audioOptionsLayout)

