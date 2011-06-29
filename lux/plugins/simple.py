from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import *

class SimplePlugin(LuxPlugin):

    # Plugin Name
    name = "Simple Plugin"

    # Plugin Description
    description = """
    A simple demo plugin showing how to draw two spinning cubes and some text using openlase.
    """

    # Constructor
    def __init__(self):

        # This is how you register a parameter with the lux engine.
        # Parameters can be controlled using OSC or in the GUI.
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 50000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/28.0
        params.off_speed = 1.0/8.0
        params.start_dwell = 8
        params.end_dwell = 6
        params.corner_dwell = 9
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 14
        params.end_wait = 29
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        ol.color3(1.0, 0.0, 1.0);
        font = ol.getDefaultFont()
        s = "Lux!"
        w = ol.getStringWidth(font, 0.2, s)
        ol.drawString(font, (-w/2,0.1), 0.2, s)

        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))

        for i in range(2):

            if (i == 1):
                ol.color3(1.0,1.0,0.0);
            else:
                ol.color3(0.0,1.0,1.0);
                    
            ol.scale3((0.6, 0.6, 0.6))
            ol.rotate3Z(lux.time * pi * 0.1 * lux.simple_rate)
            ol.rotate3X(lux.time * pi * 0.8 * lux.simple_rate)
            ol.rotate3Y(lux.time * pi * 0.73 * lux.simple_rate)
            
            ol.begin(ol.LINESTRIP)
            ol.vertex3((-1, -1, -1))
            ol.vertex3(( 1, -1, -1))
            ol.vertex3(( 1,  1, -1))
            ol.vertex3((-1,  1, -1))
            ol.vertex3((-1, -1, -1))
            ol.vertex3((-1, -1,  1))
            ol.end()

            ol.begin(ol.LINESTRIP);
            ol.vertex3(( 1,  1,  1))
            ol.vertex3((-1,  1,  1))
            ol.vertex3((-1, -1,  1))
            ol.vertex3(( 1, -1,  1))
            ol.vertex3(( 1,  1,  1))
            ol.vertex3(( 1,  1, -1))
            ol.end()

            ol.begin(ol.LINESTRIP)
            ol.vertex3(( 1, -1, -1))
            ol.vertex3(( 1, -1,  1))
            ol.end()

            ol.begin(ol.LINESTRIP)
            ol.vertex3((-1,  1,  1))
            ol.vertex3((-1,  1, -1))
            ol.end()
