#copyright ben lipkowitz 2011
#derived from works by Toms Baugis and Michael Broxton
#copyright license: GNU GPL 2
from __future__ import division
from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import *
import math
from numpy.random import random

class SimplePlugin(LuxPlugin):
    name = "Daisy"
    description = """
    A Daisy-like pattern
    """
    def __init__(self):
        self.NUM_CIRCLES = 4
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))
        self.scale = 2.0
        self.max_segments = 20 #tweak according to openlase calibration parameters; too high can cause ol to crash
        self.max_cycles = 2 # set high (~50) for maximum glitch factor
        self.time_scale = 0.4
        self.R = 0.25 # big steps
        self.R_frequency =  1/100
        self.r = 0.08 # little steps
        self.r_frequency = 1/370
        self.p = 0.5 # size of the ring
        self.p_frequency = 1/2000
        self.color_time_frequency = 1/10
        self.color_length_frequency = 0 #3/240 #set to 0 to calibrate color
        self.color_angle_frequency = 0.1
        self.spatial_resonance = 3 #ok why is this 5 and not 4?
        self.spatial_resonance_amplitude = 0.1 
        self.spatial_resonance_offset = 0.25
        self.color_phases = random(self.NUM_CIRCLES)*6
        self.z_rotations = random(self.NUM_CIRCLES) * 0.22
        self.y_rotations = random(self.NUM_CIRCLES) * 0.24
        self.x_rotations = random(self.NUM_CIRCLES) * 0.33
        
        self.r_prime = 3 #37 
        self.g_prime = 2 #23 
        self.b_prime = 1 #128 
        
        self.scale = 2
        self.width = self.scale
        self.height = self.scale
        self.bass = 1 # plz hack this to do fft power binning kthx
        #note to self, could modulate radius with average of n_samples/n_segments

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 50000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/15.0
        params.off_speed = 1.0
        params.start_dwell = 0
        params.end_dwell = 0
        params.corner_dwell = 0
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 0
        params.end_wait = 54
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    def draw(self):
        time = lux.time
        ctf = self.color_time_frequency
        clf = self.color_length_frequency
        caf = self.color_angle_frequency/2
        theta0 = abs(math.sin(time*self.time_scale))

        
        for braid_count in range(1,self.NUM_CIRCLES):
            first = True
            n = 0
            theta = theta0
            
            ol.color3(1.0, 0.0, 1.0);
            ol.loadIdentity3()
            ol.loadIdentity()
            ol.perspective(40, 1, 1, 100)
            ol.translate3((0, 0, -3))
            ol.rotate3Z(lux.time * pi * self.z_rotations[braid_count])
            ol.rotate3X(lux.time * pi * self.x_rotations[braid_count])
            ol.rotate3Z(lux.time * pi * self.x_rotations[braid_count])

            ol.begin(ol.LINESTRIP)
            while theta < theta0 + 2*pi:

                r = (0.5+sin(10*theta)/2.0) / float(braid_count) * self.scale
                x = r * cos(theta)
                y = r * sin(theta)

                angle = math.atan2(y, x)/(2*pi)
                red   = abs(math.sin(2*pi*(self.r_prime/3+ctf*time+clf*n+caf*angle)+self.color_phases[braid_count]))
                green = abs(math.sin(2*pi*(self.g_prime/3+ctf*time+clf*n+caf*angle)+self.color_phases[braid_count]))
                blue =  abs(math.sin(2*pi*(self.b_prime/3+ctf*time+clf*n+caf*angle)+self.color_phases[braid_count]))
                ol.color3(red, green, blue)
                ol.vertex3((x,y,0))
                n += 1

                theta += 1.0/float(self.max_segments)

            r = (0.5+sin(10*theta)/2.0) / float(braid_count) * self.scale
            x = r * cos(theta)
            y = r * sin(theta)
            ol.vertex3((x,y,0))  # Close the path
            ol.end()



