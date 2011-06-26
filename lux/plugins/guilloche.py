#derived from works by Toms Baugis and Michael Broxton
#copyright license: GNU GPL 2
from __future__ import division
from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import pi
import math

class SimplePlugin(LuxPlugin):
    name = "Guilloche"
    description = """
    A spirograph-like pattern
    """
    def __init__(self):
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))
        #eventually i'll port these to lux parameters, but right now there doesn't seem to be any reason to
        self.max_segments = 400 #tweak according to openlase calibration parameters; too high can cause ol to crash
        self.max_cycles = 15 # set high (~50) for maximum glitch factor
        self.time = 0
        self.time_step = 1/30
        self.time_scale = 1/1
        self.theta_step = 0.01
        self.R = 0.25 # big steps
        self.R_period = 1/100
        self.r = 0.08 # little stepsi
        self.r_period = 1/37
        self.p = 0.5 # size of the ringa
        self.p_period = 1/6
        self.scale = 5
        self.width = self.scale
        self.height = self.scale
        self.bass = 0 # plz hack this to do fft kthx
    def draw(self):
        time = lux.time
        theta = math.sin(time*self.time_scale)
        R = self.R * math.sin(time*self.time_scale*self.R_period)
        r = self.r * math.sin(time*self.time_scale*self.r_period)
        p = self.p * math.sin(time*self.time_scale*self.p_period) * self.bass

        ol.color3(1.0, 0.0, 1.0);
        ol.loadIdentity3()
        ol.loadIdentity()
        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))
        
        first = True
        n = 0
        while theta < 2 * math.pi * self.max_cycles and n < self.max_segments:
            theta += self.theta_step
            x = (R + r) * math.cos(theta) + (r + p) * math.cos((R+r)/r * theta)
            y = (R + r) * math.sin(theta) + (r + p) * math.sin((R+r)/r * theta)
            
            x *= self.width
            y *= self.height
            if first:
                ol.begin(ol.LINESTRIP)
                ol.vertex3((x,y,0))
                first = False
            ol.color3(math.sin(time*n/37), math.cos(time*n/23), math.tan(time*n/128))
            ol.vertex3((x,y,0))
            n += 1
        ol.end()
        #dynamically adjust resolution
        target = self.max_segments * 0.8
        error = (target - n)/target
        self.theta_step = min(max(1e-100, self.theta_step * (1-error)), 1)
        print n
        #self.time += self.time_step
#        self.theta_step = self.theta_step -0.0000003
        #self.theta_step = self.theta_step -0.00003

       
        #test square
        if False:
            ol.begin(ol.LINESTRIP)
            ol.vertex3((0,1,0))
            ol.vertex3((1,1,0))
            ol.vertex3((1,0,0))
            ol.vertex3((0,0,0))
            ol.end()
        
        if False:            
            ol.scale3((0.6, 0.6, 0.6))
            ol.rotate3Z(lux.time * pi * 0.1 * lux.simple_rate)
            ol.rotate3X(lux.time * pi * 0.8 * lux.simple_rate)
            ol.rotate3Y(lux.time * pi * 0.73 * lux.simple_rate)
