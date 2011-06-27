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

    def __init__(self, audio_engine, video_engine, parent = None):
        QtCore.QThread.__init__(self, parent)

        self.settings = LuxSettings()
        self.ol_update_params = True

        self.settings['video'].refreshWithDefault('videoMode', False)
        self.settings['video'].refreshWithDefault('threshold', 0.2 * 99.0)
        self.settings['video'].refreshWithDefault('blur', 1.5 / 5.0 * 99.0)
        self.settings['video'].refreshWithDefault('minArea', 100 / (640*480) * 99.0)
        self.settings['video'].refreshWithDefault('maxArea', 99.0)
        self.settings['video'].refreshWithDefault('maxNum', 10)
        
        # Initialize OpenLase
        if (ol.init(3, 96000) != 0):
            raise Exception("Could not initialize openlase")

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

        self.current_plugin_key = None
        self.current_plugin = None
        self.random_plugin()

    def __del__(self):
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
        while not self.exiting:
            self.lock.lock()

            # Check to see if we need to update OL parameters
            if (self.ol_update_params):
                params = ol.getRenderParams()
                params.rate = self.settings['calibration'].olRate
                params.on_speed = 1.0/self.settings['calibration'].olOnSpeed
                params.off_speed = 1.0/self.settings['calibration'].olOffSpeed
                params.start_wait = self.settings['calibration'].olStartWait
                params.start_dwell = self.settings['calibration'].olStartDwell
                params.curve_dwell = self.settings['calibration'].olCurveDwell
                params.corner_dwell = self.settings['calibration'].olCornerDwell
                params.curve_angle = math.cos(30.0*(math.pi/180.0)); # 30 deg
                params.end_dwell = self.settings['calibration'].olEndDwell
                params.end_wait = self.settings['calibration'].olEndWait
                params.snap = 1/100000.0;
                #	params.render_flags = ol.RENDER_NOREORDER;
                ol.setRenderParams(params)
                self.ol_update_params = False
                


            
            if (self.current_plugin):

                if (self.settings['video'].videoMode):
                    self.video_engine.draw_lasers()
                else:
                    self.current_plugin.draw()

                frame_render_time = ol.renderFrame(60)   # Takes max_fps as argument
                frames += 1
                ftime += frame_render_time
                #print "Frame time: %f, FPS:%f"%(frame_render_time, frame_render_time/ftime)
            else:
                time.sleep(0.1)
            self.lock.unlock()
            
    # ---------------  METHODS CALLED BY OTHER THREADS ----------------

    def exit(self):
        print '\t--> Shutting down Lux Engine.'
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
        self.current_plugin_key = key
        self.current_plugin = LuxPlugin.plugins[self.current_plugin_key]()

    def list_plugins(self):
        self.lock.lock()
        keys = LuxPlugin.plugins.keys()
        full_names = [(lambda k: LuxPlugin.plugins[k].name)(key) for key in keys]
        descriptions = [(lambda k: LuxPlugin.plugins[k].description)(key) for key in keys]
        self.lock.unlock()
        return (keys, full_names, descriptions)

    def updateOlParams(self):
        self.ol_update_params = True
