from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import *

class SimplePlugin(LuxPlugin):

    # Plugin Name
    name = "Davidad's plugin"

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
        s = "davidad"
	x = sin(lux.time)*0.5;
        w = ol.getStringWidth(font, x, s)
        #ol.drawString(font, (-w/2,0), x, s)

        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))

        t = lux.time*2
        lx = 0
        ly = 0
        for i in range(8):

            c = floor(t*2+i)%3
            c = 3
            if (c==1):
	    #if(1):
                ol.color3(1.0,1.0,0.0);
            if (c==2):
                ol.color3(0.0,1.0,1.0);
            if (c==3):
                ol.color3(1.0,0.0,1.0);
                    
            ol.scale3((0.6, 0.6, 0.6))
            #ol.rotate3Z(lux.time * pi * 0.1 * lux.simple_rate)
            #ol.rotate3X(lux.time * pi * 0.8 * lux.simple_rate)
            #ol.rotate3Y(lux.time * pi * 0.73 * lux.simple_rate)

	    z = 2*sin(t*2)
            z = -1+4*(t*2-floor(t*2))
            #z = 4
            x = 0.5*sin(t+i/1.0);
            y = 0.5*cos(t+i/1.0);

            ol.begin(ol.LINESTRIP)
            ol.vertex3((x-1,y-1,z))
            ol.vertex3((x-1,y+1,z))
            ol.vertex3((x+1,y+1,z))
            ol.vertex3((x+1,y-1,z))
            ol.vertex3((x-1,y-1,z))
            ol.end()

            if i != 0:
                ol.begin(ol.LINESTRIP)
                ol.vertex3((x-1,y-1,z))
                ol.vertex3((lx-1,ly-1,z+4))
                ol.end()
            
                ol.begin(ol.LINESTRIP)
                ol.vertex3((x-1,y+1,z))
                ol.vertex3((lx-1,ly+1,z+4))
                ol.end()
            
                ol.begin(ol.LINESTRIP)
                ol.vertex3((x+1,y+1,z))
                ol.vertex3((lx+1,ly+1,z+4))
                ol.end()
            
                ol.begin(ol.LINESTRIP)
                ol.vertex3((x+1,y-1,z))
                ol.vertex3((lx+1,ly-1,z+4))
                ol.end()

            lx = x
            ly = y
            
            #ol.begin(ol.LINESTRIP)
            #ol.vertex3((-1, -1, -1))
            #ol.vertex3(( 1, -1, -1))
            #ol.vertex3(( 1,  1, -1))
            #ol.vertex3((-1,  1, -1))
            #ol.vertex3((-1, -1, -1))
            #ol.vertex3((-1, -1,  1))
            #ol.end()

            #ol.begin(ol.LINESTRIP);
            #ol.vertex3(( 1,  1,  1))
            #ol.vertex3((-1,  1,  1))
            #ol.vertex3((-1, -1,  1))
            #ol.vertex3(( 1, -1,  1))
            #ol.vertex3(( 1,  1,  1))
            #ol.vertex3(( 1,  1, -1))
            #ol.end()

            #ol.begin(ol.LINESTRIP)
            #ol.vertex3(( 1, -1, -1))
            #ol.vertex3(( 1, -1,  1))
            #ol.end()

            #ol.begin(ol.LINESTRIP)
            #ol.vertex3((-1,  1,  1))
            #ol.vertex3((-1,  1, -1))
            #ol.end()
