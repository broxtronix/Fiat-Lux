from lux_plugin import LuxPlugin, ColorDriftPlugin
import pylase as ol
from audio import audio_engine

from parameters import lux, Parameter
from math import *
import numpy as np
import colorsys
import random

class Scope(LuxPlugin, ColorDriftPlugin):

    # Plugin Name
    name = "Oscilloscope"

    # Plugin Description
    description = """
    Oscilloscope plugin for rendering audio.
    """

    # Constructor
    def __init__(self):
        LuxPlugin.__init__(self)
        ColorDriftPlugin.__init__(self)

        # Reset things
        audio_engine.clear_all()
        self.x_coord = -1.0
        self.step = 1/256.0
        self.subsamp = 2
        self.sample_array = np.zeros(512)

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 50000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1
        params.off_speed = 1
        params.start_dwell = 0
        params.end_dwell = 0
        params.corner_dwell = 0
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 1
        params.end_wait = 1
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        # Grab the raw audio buffers
        mono = audio_engine.left_buffer()
#        mono = np.zeros(512)

        # Make sure they aren't empty!!
        if (mono.shape[0] == 0):
            return

        # Openlase can only draw 30000 points in one cycle (less that
        # that, actually!).  Clear the audio buffer and try again!
        if mono.shape[0] > 10000:
            audio_engine.clear_all()
 
        ol.loadIdentity3()
        ol.color3(*(self.color_cycle()))

        count = 0
        while count < mono.shape[0]:

            ol.begin(ol.LINESTRIP)
            while self.x_coord < 1.0 and count < mono.shape[0]:

                scale_factor = pow(1.0-abs(self.x_coord),0.5)*2
                #ol.vertex3((self.x_coord, mono[count]*scale_factor, -1))             # Linear
                ol.vertex3((self.x_coord, tanh(mono[count]*scale_factor), -1))        # Tanh
                #ol.vertex3((self.x_coord, log(mono[count]*scale_factor+1.0), -1))    # Sigmoid
                
                self.x_coord += self.step
                count = count + self.subsamp
            ol.end()

            if self.x_coord >= 1.0:
                self.x_coord = -1.0
                
        ol.end()
