from PyQt4 import QtCore, QtGui
import time
import random
import math

import pylase as ol
from parameters import lux, Parameter
from settings import LuxSettings

import plugins
from plugins.lux_plugin import LuxPlugin
    
class LuxEngine(QtCore.QThread):

    def __init__(self, audio_engine, video_engine, output_engine, parent = None):
        QtCore.QThread.__init__(self, parent)

        self.settings = LuxSettings()
        self.ol_update_params = True

        self.settings['video'].refreshWithDefault('videoMode', False)
        self.settings['video'].refreshWithDefault('threshold', 0.2 * 99.0)
        self.settings['video'].refreshWithDefault('blur', 1.5 / 5.0 * 99.0)
        self.settings['video'].refreshWithDefault('minArea', 100 / (640*480) * 99.0)
        self.settings['video'].refreshWithDefault('maxArea', 99.0)
        self.settings['video'].refreshWithDefault('maxNum', 10)
        

        self.settings['calibration'].refreshWithDefault('parameterOverride', False)
        self.settings['calibration'].refreshWithDefault('olRate', 30000 / 30000.0 * 99.0)
        self.settings['calibration'].refreshWithDefault('olOnSpeed', 100)
        self.settings['calibration'].refreshWithDefault('olOffSpeed', 20)
        self.settings['calibration'].refreshWithDefault('olStartDwell', 3)
        self.settings['calibration'].refreshWithDefault('olEndDwell', 3)
        self.settings['calibration'].refreshWithDefault('olCornerDwell', 4)
        self.settings['calibration'].refreshWithDefault('olCurveDwell', 0)
        self.settings['calibration'].refreshWithDefault('olStartWait', 8)
        self.settings['calibration'].refreshWithDefault('olEndWait', 7)
        
        # create a mutex and semaphore for managing this thread.
        self.lock = QtCore.QMutex()
        self.exiting = False

        self.audio_engine = audio_engine
        self.video_engine = video_engine
        self.output_engine = output_engine

        self.current_plugin_key = None
        self.current_plugin = None
        self.random_plugin()

    def __del__(self):
        self.output_engine.setOutputInitialized(False)  # Turn on the hardware safety interlock
        self.exiting = True
        self.wait()

        # Shut down OpenLase
        ol.shutdown()

    # Note: This is never called directly. It is called by Qt once the
    # thread environment has been set up.
    def run(self):

        # Run the render loop.  This will repeatedly render frames of the current plugin.
        print '\t--> Starting up LUX Engine.'
        ftime = 0
        frames = 0

        # Initialize OpenLase.  This also creates the lux_engine jack endpoints.
        if (ol.init(3, 96000) != 0):
            raise Exception("Could not initialize openlase")

        # Connect the output engine to the lux_engine.
        self.output_engine.connect_ports("lux_engine:out_x", "lux_output:in_x")
        self.output_engine.connect_ports("lux_engine:out_y", "lux_output:in_y")
        self.output_engine.connect_ports("lux_engine:out_r", "lux_output:in_r")
        self.output_engine.connect_ports("lux_engine:out_g", "lux_output:in_g")
        self.output_engine.connect_ports("lux_engine:out_b", "lux_output:in_b")

        # Turn off the hardware safety interlock.
        self.output_engine.setOutputInitialized(True)

        # Create a local settings object for this thread.
        settings = LuxSettings()
        
        while not self.exiting:
            # Grab local references to these class variables
            self.lock.lock()
            current_plugin = self.current_plugin
            video_engine = self.video_engine
            self.lock.unlock()
            
            # SET PARAMETERS
            #
            # Check to see if the GUI parameter override has been set,
            # and we need to update OL parameters.
            if (self.ol_update_params and settings['calibration'].parameterOverride and current_plugin):
                current_plugin.setParametersToGuiValues()
                self.ol_update_params = False

            if (current_plugin and not settings['calibration'].parameterOverride):
                current_plugin.setParameters();

            # RENDER
            #
            # We call out to the current plugin's draw() method, or
            # the video plugin, depending on the current state of the
            # GUI.
            if (current_plugin):
                if (settings['video'].videoMode):
                    video_engine.draw_lasers()
                else:
                    current_plugin.draw()

                frame_render_time = ol.renderFrame(60)   # Takes max_fps as argument
                frames += 1
                ftime += frame_render_time
                #print "Frame time: %f, FPS:%f"%(frame_render_time, frame_render_time/ftime)
            else:
                # If there is no plugin for some reason, kill time
                # rather than burning CPU in a loop that does nothing.
                time.sleep(0.1)
            
    # ---------------  METHODS CALLED BY OTHER THREADS ----------------

    def exit(self):
        print '\t--> Shutting down Lux Engine.'
        self.output_engine.setOutputInitialized(False)  # Turn on the hardware safety interlock
        self.exiting = True
        self.wait()

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

    def select_plugin(self, key):
        self.lock.lock()
        self.current_plugin_key = key
        self.current_plugin = LuxPlugin.plugins[self.current_plugin_key]()
        self.lock.unlock()

    def list_plugins(self):
        self.lock.lock()
        keys = LuxPlugin.plugins.keys()
        full_names = [(lambda k: LuxPlugin.plugins[k].name)(key) for key in keys]
        descriptions = [(lambda k: LuxPlugin.plugins[k].description)(key) for key in keys]
        self.lock.unlock()
        return (keys, full_names, descriptions)

    def updateOlParams(self):
        self.ol_update_params = True
