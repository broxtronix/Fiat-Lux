from lux_plugin import LuxPlugin
import pylase as ol
from audio import audio_engine

from parameters import lux, Parameter
from math import *

class TwoCubes(LuxPlugin):

    # Plugin Name
    name = "Two Cubes"

    # Plugin Description
    description = """
    Two cubes, moving as a function of time!
    """

    # Constructor
    def __init__(self):
        # This is how you register a parameter with the lux engine.
        # Parameters can be controlled using OSC or in the GUI.
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))
        
    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        for i in range(2):
            ol.loadIdentity3()
            ol.perspective(20, 1, 1, 100)
            ol.translate3((0, 0, -20))

            if (i == 1):
                ol.color3(1.0,1.0,0.0);
                ol.translate3((cos(lux.time/2.0), cos(lux.time/3.0), cos(lux.time/7.0)))
                ol.rotate3Z(lux.time * pi * 0.1 * lux.simple_rate)
                ol.rotate3X(lux.time * pi * 0.25 * lux.simple_rate)
                ol.rotate3Y(lux.time * pi * 0.13 * lux.simple_rate)
            else:
                ol.color3(0.0,1.0,1.0);
                ol.scale3((0.6, 0.6, 0.6))
                ol.translate3((cos(lux.time/3.2), cos(lux.time/2.6), cos(lux.time/5.4)))
                ol.rotate3Z(lux.time * pi * 0.14 * lux.simple_rate)
                ol.rotate3X(lux.time * pi * 0.53 * lux.simple_rate)
                ol.rotate3Y(lux.time * pi * 0.22 * lux.simple_rate)
            
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
