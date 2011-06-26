from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import pi,sin

class TestPatternPlugin(LuxPlugin):

    # Plugin Name
    name = "Test Pattern"

    # Plugin Description
    description = """
    A bounding box with crosshair.
    """

    def __init__(self):
        pass

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
        
