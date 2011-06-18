from PyQt4 import QtCore, QtGui
import time
import random

import pylase as ol
from parameters import lux, Parameter
import plugins
from plugins.lux_plugin import LuxPlugin

class LuxEngine(QtCore.QThread):

    def __init__(self, audio_engine, parent = None):
        QtCore.QThread.__init__(self, parent)

        # create a mutex and semaphore for managing this thread.
        self.lock = QtCore.QMutex()
        self.exiting = False

        self.audio_engine = audio_engine

        print "\t-->Loaded these plugins:"
        print self.list_plugins()
        self.current_plugin = None
        self.random_plugin()
        print self.current_plugin

    def __del__(self):
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
            self.lock.lock()
            if (self.current_plugin):
                self.current_plugin.draw()

                frame_render_time = ol.renderFrame(60)   # Takes max_fps as argument
                frames += 1
                ftime += frame_render_time
                #print "Frame time: %f, FPS:%f"%(frame_render_time, frame_render_time/ftime)
            else:
                time.sleep(0.1)
            self.lock.unlock()
            
        # Shut down OpenLase
        ol.shutdown()

    # ---------------  METHODS CALLED BY OTHER THREADS ----------------

    def exit(self):
        print '\t--> Shutting down Lux Engine.'
        self.exiting = True
        self.wait()

    def next_plugin(self):
         self.lock.lock()

         self.lock.unlock()

    # Choose a random plugin from the list of those that have been loaded.
    def prev_plugin(self):
         self.lock.lock()
         
         self.lock.unlock()

    # Choose a random plugin from the list of those that have been loaded.
    def random_plugin(self):
         self.lock.lock()
         if len(LuxPlugin.plugins) == 0:
             self.current_plugin = None
         else:
             keys = LuxPlugin.plugins.keys()
             self.current_plugin_key = random.choice(keys)
             self.current_plugin = LuxPlugin.plugins[self.current_plugin_key]()
         self.lock.unlock()

    def list_plugins(self):
        keys = LuxPlugin.plugins.keys()
        return [(lambda k: LuxPlugin.plugins[k].name)(key) for key in keys]
