from lux_plugin import LuxPlugin, ColorDriftPlugin
import pylase as ol
from audio import audio_engine

from parameters import lux, Parameter
from math import *
import numpy as np
import colorsys
import random

class CircleScope(LuxPlugin, ColorDriftPlugin):

    # Plugin Name
    name = "Circlescope (Openlase)"

    # Plugin Description
    description = """
    The original openlase circlescope plugin.
    """

    # Constructor
    def __init__(self):
        LuxPlugin.__init__(self)
        ColorDriftPlugin.__init__(self)

        # Reset things
        audio_engine.clear_all()

        # Constants
        self.SUBSAMP = 20
        self.BOOST = 8
        self.MIN_SIZE = 0.2
        self.MAX_SIZE = 1.0

        self.W = 523.251131 / 4.0 * pi;
        self.pos = 0.0
        self.mono = None

    # Slow, random evolution of hue. 
    def color_cycle(self):
        if (abs(self.hue_target - self.current_hue) < self.hue_step):
            self.hue_target = random.random()
        
        if (self.hue_target > self.current_hue):
            self.current_hue = self.current_hue + self.hue_step
        else:
            self.current_hue = self.current_hue - self.hue_step
            
        return colorsys.hsv_to_rgb(self.current_hue, 1.0, 1.0)

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        # Grab the raw audio buffers
        newbuffer = audio_engine.mono_buffer()

        # Make sure they aren't empty!!
        if (len(newbuffer) == 0):
            return
        else:
            self.mono = newbuffer

        # Openlase can only draw 30000 points in one cycle (less that
        # that, actually!).  Clear the audio buffer and try again!
        if self.mono.shape[0] > 10000:
            audio_engine.clear_all()

        ol.loadIdentity3()
        ol.color3(*(self.color_cycle()))

        ol.begin(ol.POINTS)
        for i in range(0, self.mono.shape[0]-1, self.SUBSAMP):

            val = tanh(self.mono[i] * self.BOOST)
            val = val * 0.5 + 0.5
            val = val * (self.MAX_SIZE - self.MIN_SIZE) + self.MIN_SIZE
            
            ol.vertex3((cos(self.pos) * val, sin(self.pos) * val, -1))
            
            self.pos = self.pos + self.W / 30000.0;
            while(self.pos >= 2*pi):
                self.pos = self.pos -2*pi
        ol.end()
