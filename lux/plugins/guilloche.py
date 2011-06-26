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
    A spirograph-like pattern.
    Set crn_dwell and crv_dwell to 0!
    """
    def __init__(self):
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))
        #eventually i'll port these to lux parameters, but right now there doesn't seem to be any reason to since there are no GUI sliders
        self.max_segments = 300 #tweak according to openlase calibration parameters; too high can cause ol to crash
        self.max_cycles = 10 # set high (~50) for maximum glitch factor
        self.time = 1
        self.time_step = 1/30
        self.time_scale = 1/1
        self.theta_step = 0.01
        self.R = 0.25 # big steps
        self.R_frequency = 1/100
        self.r = 0.08 # little steps
        self.r_frequency = 1/37
        self.p = 0.5 # size of the ring
        self.p_frequency = 1/2000
        self.color_time_frequency = 1/4
        self.color_length_frequency = 1/240 #set to 0 to calibrate color
        self.color_angle_frequency = 1
        self.r_prime = 1 #37
        self.g_prime = 2 #23
        self.b_prime = 3 #128
        
        self.scale = 3
        self.width = self.scale
        self.height = self.scale
        self.bass = 1 # plz hack this to do fft power binning kthx

    def draw(self):
        time = lux.time
        time = self.time
        ctf = self.color_time_frequency
        clf = self.color_length_frequency
        caf = self.color_angle_frequency
        theta = math.sin(time*self.time_scale)
        R = self.R * math.sin(2*pi*time*self.time_scale*self.R_frequency)
        r = self.r * math.sin(2*pi*time*self.time_scale*self.r_frequency)
        p = self.p * math.sin(2*pi*time*self.time_scale*self.p_frequency) * self.bass

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
                first = False
            #red = math.sin(ctf*time*n/37) * math.sin(csf*theta*n/37)
            #green = math.sin(ctf*time*n/23) * math.sin(csf*theta*n/23)
            #blue = math.sin(ctf*time*n/128) * math.sin(csf*theta*n/128)
            
            angle = math.atan2(y, x)/(2*pi)
            red   = math.sin(2*pi*(self.r_prime/3+ctf*time+clf*n+caf*angle))
            green = math.sin(2*pi*(self.g_prime/3+ctf*time+clf*n+caf*angle))
            blue =  math.sin(2*pi*(self.b_prime/3+ctf*time+clf*n+caf*angle))

            ol.color3(red, green, blue)
            ol.vertex3((x,y,0))
            n += 1
        ol.end()
        #dynamically adjust resolution
        target = self.max_segments * 0.8
        error = (target - n)/target
        self.theta_step = min(max(1e-100, self.theta_step * (1-error)), 1)
        print n, time
        self.time += 1/30
