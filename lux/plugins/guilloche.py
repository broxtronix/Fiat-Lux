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

class SimplePlugin(LuxPlugin):
    name = "Guilloche"
    description = """
    A spirograph-like pattern.
    Set corner dwell and curve dwell to 0!
    """
    def __init__(self):
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))
        #eventually i'll port these to lux parameters, but right now there doesn't seem to be any reason to since there are no GUI sliders
        self.max_segments = 800 #tweak according to openlase calibration parameters; too high can cause ol to crash
        self.max_cycles = 5 # set high (~50) for maximum glitch factor
        self.time = 1
        self.time_step = 1/30
        self.time_scale = 0.4
        self.theta_step = 0.01
        self.R = 0.25 # big steps
        self.R_frequency =  1/100
        self.r = 0.08 # little steps
        self.r_frequency = 1/370
        self.p = 0.5 # size of the ring
        self.p_frequency = 1/2000
        self.color_time_frequency = 1/10
        self.color_length_frequency = 0 #3/240 #set to 0 to calibrate color
        self.color_angle_frequency = 0.5
        self.spatial_resonance = 3 #ok why is this 5 and not 4?
        self.spatial_resonance_amplitude = 0.1 
        self.spatial_resonance_offset = 0.25
        
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
        params.rate = 30000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/1.0
        params.off_speed = 1.0/6.0
        params.start_dwell = 10
        params.end_dwell = 8
        params.corner_dwell = 0
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 11
        params.end_wait = 7
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    def draw(self):
        time = lux.time
        #time = self.time
        ctf = self.color_time_frequency
        clf = self.color_length_frequency
        caf = self.color_angle_frequency/2
        theta = abs(math.sin(time*self.time_scale))
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
        while theta < 2*pi*self.max_cycles and n < self.max_segments:
            theta += self.theta_step
            #x = (R + r) * math.cos(theta)
            #y = (R + r) * math.sin(theta)
            x = (R + r) * math.cos(theta) + (r + p) * math.cos((R+r)/r * theta)
            y = (R + r) * math.sin(theta) + (r + p) * math.sin((R+r)/r * theta)
            
            if first:
                ol.begin(ol.LINESTRIP)
                #ol.begin(ol.POINTS)
                first = False
            #red = math.sin(ctf*time*n/37) * math.sin(csf*theta*n/37)
            #green = math.sin(ctf*time*n/23) * math.sin(csf*theta*n/23)
            #blue = math.sin(ctf*time*n/128) * math.sin(csf*theta*n/128)
            
            angle = math.atan2(y, x)/(2*pi)
            red   = abs(math.sin(2*pi*(self.r_prime/3+ctf*time+clf*n+caf*angle)))
            green = abs(math.sin(2*pi*(self.g_prime/3+ctf*time+clf*n+caf*angle)))
            blue =  abs(math.sin(2*pi*(self.b_prime/3+ctf*time+clf*n+caf*angle)))
            ol.color3(red, green, blue)
            
            #this makes it square-ish
            #x += math.cos(2*pi*angle*self.spatial_resonance)*self.spatial_resonance_amplitude
            #y += math.sin(2*pi*angle*self.spatial_resonance)*self.spatial_resonance_amplitude
            x += math.cos(2*pi*angle*(self.spatial_resonance+1)+2*pi*self.spatial_resonance_offset)*self.spatial_resonance_amplitude
            y += math.sin(2*pi*angle*(self.spatial_resonance+1)+2*pi*self.spatial_resonance_offset)*self.spatial_resonance_amplitude


            x *= self.width
            y *= self.height
            ol.vertex3((x,y,0))
            n += 1
        ol.end()
        #dynamically adjust resolution
        target = self.max_segments * 0.8
        error = (target - n)/target
        self.theta_step = min(max(1e-100, self.theta_step * (1-error)), 1)
        #print n,  angle
        self.time += 1/30

