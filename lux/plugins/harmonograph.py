from lux_plugin import LuxPlugin, ColorDriftPlugin
import pylase as ol
from audio import audio_engine

from parameters import lux, Parameter
from math import *
import numpy as np
import colorsys
import random

class HarmonographPlugin(LuxPlugin, ColorDriftPlugin):

    # Plugin Name
    name = "Harmonograph"

    # Plugin Description
    description = """
    Harmonograph plugin
    """

    # Constructor
    def __init__(self):
        LuxPlugin.__init__(self)
        ColorDriftPlugin.__init__(self)

        # Parameters
        self.SAMPLES_PER_FRAME = 900
        self.MAX_THETA = 16 * pi
        self.RATE = 0.2

        self.x_ratio = 3
        self.x_phase = 0
        self.y_ratio = 5
        self.y_phase = 0
        self.z_ratio = 7
        self.z_phase = 0
        self.decay = 0.9995

        self.spin = 0
        self.spin_phase = 0

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 30000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/1.0
        params.off_speed = 1.0/1.0
        params.start_dwell = 1
        params.end_dwell = 1
        params.corner_dwell = 0
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 12
        params.end_wait = 11
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    # The draw method gets called roughly 30 times a second.  
    def draw(self):

        self.x_phase = 0.4*cos(1.7 * lux.time * self.RATE) + 0.6*cos(0.7 * lux.time * self.RATE)
        self.y_phase = cos(2.2 * lux.time * self.RATE)
        self.z_phase = cos(5.7 * lux.time * self.RATE)
        self.z_ratio = 2 + cos(0.1 * lux.time * self.RATE)

        ol.loadIdentity3()
        ol.loadIdentity()

        ol.perspective(20, 1, 1, 100)
        ol.translate3((0, 0, -10))

        ol.rotate3Z(lux.time * pi * 0.01)
        ol.rotate3X(lux.time * pi * 0.025)
        ol.rotate3Y(lux.time * pi * 0.013)


        ol.color3(*(self.color_cycle()))

        ol.begin(ol.POINTS)
        decay_factor = 1
        first_point = None
        for i in range(self.SAMPLES_PER_FRAME):
            theta = float(i) / self.SAMPLES_PER_FRAME * self.MAX_THETA
            x = sin(self.x_ratio * theta + self.x_phase)
            y = sin(self.y_ratio * theta + self.y_phase)
            z = sin(self.z_ratio * theta + self.z_phase)
            if (i == 0):
                first_point = (x * decay_factor, y * decay_factor, z * decay_factor)
            ol.vertex3((x * decay_factor, y * decay_factor, z * decay_factor))
            decay_factor = decay_factor * self.decay
        ol.vertex3(first_point)
        ol.end()
        
