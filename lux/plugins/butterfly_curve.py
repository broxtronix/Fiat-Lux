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
        self.MAX_THETA = 8.0 * pi
        self.SAMPLES_PER_FRAME = 100

        self.RATE = 0.2
        self.last_time = 0
        self.test = 0

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        delta = 0.03
        self.last_time = lux.time

        self.test = self.test + delta / 10.0 * self.RATE
        while(self.test > 2 * pi):
            self.test = self.test - 2*pi

        #        print lux.time, cos(lux.time / 10.0 * self.RATE)
        self.a = 3.1 * cos(lux.time / 10.0 * self.RATE)
        self.b = 9 * sin(lux.time / 7.0 * self.RATE) + 10
        self.c = 30 * cos(lux.time / 11.0 * self.RATE)
        self.A = 1
        self.overall_amplitude = 0.5


        # self.a = 3.1 + 3.0 * cos(lux.time / 10 * self.RATE)
        # self.b = 15 + 10 * sin(lux.time / 7 * self.RATE)
        # self.c = 25 + 20 * cos(lux.time / 11 * self.RATE)
        # self.A = 0.8#  + 0.5*sin(lux.time/21.0 * self.RATE)
        # self.overall_amplitude = 0.5

        ol.loadIdentity3()
        ol.loadIdentity()
        ol.color3(*(self.color_cycle()))

        ol.begin(ol.LINESTRIP)
        for i in range(self.SAMPLES_PER_FRAME):
            theta = float(i) / self.SAMPLES_PER_FRAME * self.MAX_THETA
            r = exp(cos(self.a * theta)) - self.A * cos(self.b*theta) + pow(abs(sin(theta/self.c)),self.b)
            r = r / (2.7 - self.A + pow(1,self.b)) * self.overall_amplitude

            ol.vertex3((r * cos(theta), r * sin(theta), -1))
        ol.end()
        
