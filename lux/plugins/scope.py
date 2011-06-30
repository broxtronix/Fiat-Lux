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
        self.x_coord = -0.9
        self.step = 1/512.0
        self.subsamp = 3
        self.sample_array = np.zeros(512)

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        # Grab the raw audio buffers
        mono = audio_engine.mono_buffer()

        # Make sure they aren't empty!!
        if (mono.shape[0] == 0):
            return

        # Openlase can only draw 30000 points in one cycle (less that
        # that, actually!).  Clear the audio buffer and try again!
        if mono.shape[0] > 10000:
            audio_engine.clear_all()
            return

        ol.loadIdentity3()
        ol.color3(*(self.color_cycle()))

        ol.begin(ol.POINTS)
        for i in range(0, mono.shape[0]-1, self.subsamp):
            scale_factor = pow(0.9-abs(self.x_coord),0.5)
            if (mono[i] <= -1.0):
                mono[i] = 1.0
            ol.vertex3((self.x_coord, tanh(mono[i]*scale_factor), -1))
#            ol.vertex3((self.x_coord, log(mono[i]*scale_factor+1.0), -1))
            self.x_coord = self.x_coord + self.step
            if (self.x_coord > 0.9) : self.x_coord = -0.9
        ol.end()
