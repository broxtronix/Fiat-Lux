from lux_plugin import LuxPlugin, ColorDriftPlugin
import pylase as ol
from audio import audio_engine

from parameters import lux, Parameter
from math import *
import numpy as np
import colorsys
import random

class ButterflyCurvePlugin(LuxPlugin, ColorDriftPlugin):

    # Plugin Name
    name = "Butterfly Curves"

    # Plugin Description
    description = """
    Attempt at butterfly curves following this example:
    http://www.subblue.com/blog/2008/11/5/butterfly_curves
    """

    # Constructor
    def __init__(self):
        LuxPlugin.__init__(self)
        ColorDriftPlugin.__init__(self)

        # Parameters
        self.MAX_THETA = 4.0 * pi
        self.SAMPLES_PER_FRAME = 400

        self.RATE = 0.2
        self.reset()

        
    def reset(self):
        self.alpha = random.uniform(1.0,10.0)
        self.beta = random.uniform(5.0,15.0)
        self.gamma = random.uniform(10.0,50.0)
        self.rho = random.uniform(0.5, 1.5)
        self.overall_amplitude = 0.45

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 25000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/1.0
        params.off_speed = 1.0/6.0
        params.start_dwell = 13
        params.end_dwell = 20
        params.corner_dwell = 0
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 35
        params.end_wait = 20
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    # The draw method gets called roughly 30 times a second.  
    def draw(self):

        a = self.alpha * cos(lux.time / 10.0 * self.RATE)
        b = self.beta * sin(lux.time / 7.0 * self.RATE) + 10
        c = self.gamma * cos(lux.time / 11.0 * self.RATE)
        A = self.rho

        ol.loadIdentity3()
        ol.loadIdentity()
        ol.rotate3Z(lux.time * pi * 0.03)
        ol.color3(*(self.color_cycle()))

        ol.begin(ol.LINESTRIP)
        for i in range(self.SAMPLES_PER_FRAME):
            theta = float(i) / self.SAMPLES_PER_FRAME * self.MAX_THETA
            r = exp(cos(a * theta)) - A * cos(b*theta) + pow(abs(sin(theta/c)),b)
            r = r / (2.7 - A + pow(1,b)) * self.overall_amplitude

            ol.vertex3((r * cos(theta), r * sin(theta), -1))
        ol.end()
        
