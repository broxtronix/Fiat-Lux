from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine
import random

import pylase as ol
from math import *

class SimplePlugin(LuxPlugin):

    # Plugin Name
    name = "Line Sweep"

    # Plugin Description
    description = """
    Useful for fog machine demo.
    """

    # Constructor
    def __init__(self):

        # This is how you register a parameter with the lux engine.
        # Parameters can be controlled using OSC or in the GUI.
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 2.0 ))

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 50000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/18.0
        params.off_speed = 1.0/8.0
        params.start_dwell = 8
        params.end_dwell = 2
        params.corner_dwell = 10
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 42
        params.end_wait = 46
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))

        ol.color3(1.0,1.0,1.0)

        offset = cos(lux.time*10)
        ol.begin(ol.LINESTRIP)
        npts = 25
        #ol.scale3((0.5,0.5,0.5))
        for i in range(npts):
            ol.color3(float(i)/npts,1.0-float(i)/npts,(float(i)/npts+(1.0-float(i)/npts))/2.0)
            offset = 0
            mod = (i%2 * 2.0 - 1.0) * 0.99
            #ol.scale3((mod, mod, mod))
            ol.rotate3Z(lux.time * pi * 0.01 * lux.simple_rate)
            ol.vertex3((float(i)/(npts/2.0)-1.0+offset,-1.0,-1))
            ol.vertex3((float(i)/(npts/2.0)-1.0+offset,1.0,-1))

        ol.end()
