from PyQt4 import QtCore, QtGui
import time

import pylase as ol
from parameters import lux, Parameter
import plugins
from plugins.lux_plugin import LuxPlugin

class LuxEngine(QtCore.QThread):

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False

        if (len(LuxPlugin.plugins) == 0):
            self.current_plugin = None
        else: 
            self.current_plugin = LuxPlugin.plugins[0]()

    def __del__(self):
        self.exiting = True
        self.wait()

    # Called by other threads.
    def exit(self):
        print '\t--> Shutting down Lux Engine.'
        self.exiting = True
        self.wait()

    # Note: This is never called directly. It is called by Qt once the
    # thread environment has been set up.
    def run(self):

        # Initialize OpenLase
        if (ol.init() != 0):
            raise Exception("Could not initialize openlase")

        # Run the render loop.  This will repeatedly render frames of the current plugin.
        print '\t--> Starting up LUX Engine.'
        ftime = 0
        frames = 0
        while not self.exiting:
            if (self.current_plugin):
                self.current_plugin.draw()

                frame_render_time = ol.renderFrame(60)   # Takes max_fps as argument
                frames += 1
                ftime += frame_render_time
                #print "Frame time: %f, FPS:%f"%(frame_render_time, frame_render_time/ftime)
            else:
                time.sleep(0.1)
            
        # Shut down OpenLase
        ol.shutdown()
