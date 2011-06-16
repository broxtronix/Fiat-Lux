from lux_plugin import LuxPlugin
import pylase as ol

from parameters import lux, Parameter
from math import pi

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

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        ol.color3(0.0, 0.0, 1.0);
        font = ol.getDefaultFont()
        s = "Lux!"
        w = ol.getStringWidth(font, 0.2, s)
        ol.drawString(font, (-w/2,0.1), 0.2, s)

        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))

        for i in range(2):

            if (i == 1):
                ol.color3(1.0,0.0,0.0);
            else:
                ol.color3(0.0,1.0,0.0);
                    
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
