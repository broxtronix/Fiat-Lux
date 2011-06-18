"""
An OpenGL based QWidget for displaying the Fiat Lux laser simulator.
"""

from PyQt4 import QtCore, QtGui, QtOpenGL
# custom importer for ARB functions
from OpenGL import GL

from xenon_lux import LuxSimulatorEngine
from settings import LuxSettings

import math
import numpy
import Queue
import time
import sys
import os

class DisplayError(Exception):
    pass

class SimulationDisplay(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):

        # Set up to sync with double-buffer, vertical refresh.  Add Alpha and Depth buffers.
        fmt = QtOpenGL.QGLFormat()
        fmt.setSwapInterval(2)
        fmt.setDoubleBuffer(True)
        fmt.setAlpha(True)
        fmt.setDepth(True)
        QtOpenGL.QGLWidget.__init__(self, fmt, parent)

        # the display settings window
        self.displaySettings = None
        
        # set application settings
        self.settings = LuxSettings()

        # create a mutex for the state
        self.lock = QtCore.QMutex()

        # height and width of viewport
        self.width = 512
        self.height = 512

        # start up an update timer with an interval of 1ms.  This will
        # effectively draw frames as fast as the screen is updated.
        self.timerId = self.startTimer(1)
        
        # Start the simulator audio client.  Connects to JACK server,
        # which must be running.
        self.makeCurrent()
        self.simulator_engine = LuxSimulatorEngine("lux_simulator");
        self.simulator_engine.start()

        self.simulator_engine.connect_ports("lux_engine:out_y", "lux_simulator:in_y")
        self.simulator_engine.connect_ports("lux_engine:out_x", "lux_simulator:in_x")
        self.simulator_engine.connect_ports("lux_engine:out_r", "lux_simulator:in_r")
        self.simulator_engine.connect_ports("lux_engine:out_g", "lux_simulator:in_g")
        self.simulator_engine.connect_ports("lux_engine:out_b", "lux_simulator:in_b")
        
    def timerEvent(self, event):
        '''
        Call the OpenGL update function if necessary
        '''
        self.updateGL()


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
        self.simulator_engine.resize_gl(width, height)

    def paintGL(self):
        """Paint the screen"""
        self.makeCurrent()

        # Call out to the C++ code to do actual, efficient drawing
        self.simulator_engine.draw_gl()

