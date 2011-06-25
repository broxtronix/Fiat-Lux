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

        self.settings['video'].refreshWithDefault('videoMode', False)
        self.settings['video'].refreshWithDefault('threshold', 0.2 * 99.0)
        self.settings['video'].refreshWithDefault('blur', 1.5 / 5.0 * 99.0)
        self.settings['video'].refreshWithDefault('minArea', 100 / (640*480) * 99.0)
        self.settings['video'].refreshWithDefault('maxArea', 99.0)
        self.settings['video'].refreshWithDefault('maxNum', 10)
        
        # Initialize OpenLase
        if (ol.init(3,30000) != 0):
            raise Exception("Could not initialize openlase")

        # Set up rendering parameters
        params = ol.getRenderParams()
        params.rate = 48000;
	params.on_speed = 1.0/100.0;
	params.off_speed = 2.0/20.0;
	params.start_wait = 8;
	params.start_dwell = 3;
	params.curve_dwell = 0;
	params.corner_dwell = 4;
	params.curve_angle = math.cos(30.0*(math.pi/180.0)); # 30 deg
	params.end_dwell = 3;
	params.end_wait = 7;
	params.snap = 1/100000.0;
        #	params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

        # params = ol.getRenderParams()
        # params.rate = 30000;
	# params.on_speed = 1.0/100.0;
	# params.off_speed = 2.0/20.0;
	# params.start_wait = 15;
	# params.start_dwell = 15;
	# params.curve_dwell = 15;
	# params.corner_dwell = 10;
	# params.curve_angle = math.cos(30.0*(math.pi/180.0)); # 30 deg
	# params.end_dwell = 15;
	# params.end_wait = 15;
	# params.snap = 1/100000.0;
        # #	params.render_flags = ol.RENDER_NOREORDER;
        # ol.setRenderParams(params)

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
