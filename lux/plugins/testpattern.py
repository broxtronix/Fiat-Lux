from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import *

class TestPatternPlugin(LuxPlugin):

    # Plugin Name
    name = "Test Pattern"

    # Plugin Description
    description = """
    A bounding box with crosshair.
    """

    def __init__(self):
        pass

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 50000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/48.0
        params.off_speed = 1.0/7.0
        params.start_dwell = 8
        params.end_dwell = 11
        params.corner_dwell = 9
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 14
        params.end_wait = 54
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    def draw(self):
        ol.loadIdentity()

        ol.color3(1.0, 1.0, 1.0);

        # bounding box
        ol.begin(ol.LINESTRIP)
        self.square(1,1,-1,-1)
        ol.end()
        
        # horizontal line
        ol.begin(ol.LINESTRIP)
        ol.vertex((-1,0))
        ol.vertex((1,0))        
        ol.end()

        # vertical line
        ol.begin(ol.LINESTRIP)
        ol.vertex((0,-1))
        ol.vertex((0,1))        
        ol.end()

        # inner box, for fun
        ol.color3(0.0, 1.0, 0.0);
        size = (sin(lux.time) * .2)+.5
        ol.begin(ol.LINESTRIP)
        self.square(size,size,-size,-size)
        ol.end()

        # Red dots
        ol.loadIdentity()
        ol.loadIdentity3()

        ol.begin(ol.LINESTRIP)
        for y in range(0, 20):
            ol.color3(float(y)/20.0, 0.0, 0.0);
            ol.vertex3((-0.6, (float(y-10) / 12.0), -1.0))
        ol.end()

        # Green dots
        ol.begin(ol.LINESTRIP)
        for y in range(0, 20):
            ol.color3(0.0, float(y)/20.0, 0.0);
            ol.vertex3((-0.4, (float(y-10) / 12.0), -1.0))
        ol.end()

        # Blue dots
        ol.begin(ol.LINESTRIP)
        for y in range(0, 20):
            ol.color3(0.0, 0.0, float(y)/20.0);
            ol.vertex3((-0.2, (float(y-10) / 12.0), -1.0))
        ol.end()

        # vertical line
        ol.begin(ol.LINESTRIP)
        ol.vertex((0,-1))
        ol.vertex((0,1))        
        ol.end()


    def square(self,x1,y1,x2,y2):
        ol.begin(ol.LINESTRIP)
        ol.vertex((x1,y1))
        ol.vertex((x1,y2))
        ol.vertex((x2,y2))        
        ol.vertex((x2,y1))        
        ol.vertex((x1,y1))        
        ol.end()
        
