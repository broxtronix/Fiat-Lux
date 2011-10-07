from lux_plugin import LuxPlugin
import pylase as ol
from audio import audio_engine
import liblo

from parameters import lux, Parameter
from math import *

class TouchCubes(LuxPlugin):

    # Plugin Name
    name = "Touch Cubes"

    # Plugin Description
    description = """
    Cubes that appear and move around in response to OSC messages.
    """

    # Constructor
    def __init__(self):
        # This is how you register a parameter with the lux engine.
        # Parameters can be controlled using OSC or in the GUI.
        lux.register(Parameter( name = "TouchCubes_simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                namespace = "touch_cubes",
                                min_value = 0.0, max_value = 1.0, default_value = 1.0,
                                stateful = True))
        # create server, listening on port 1234
        try:
            self.server = liblo.Server(8000)
        except liblo.ServerError, err:
            print str(err)
            sys.exit()

        self.server.add_method(None, None, self.osc_callback)

    def __del__(self):
        self.tracking.stop()

    def osc_callback(self, path, args, types, src):
        print 'osc',path,args,types,src

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

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        self.server.recv(10)

        #            print 'obj',obj
        # for i in range(2):
        #     ol.loadIdentity3()
        #     ol.perspective(20, 1, 1, 100)
        #     ol.translate3((0, 0, -20))

        #     if (i == 1):
        #         ol.color3(1.0,1.0,0.0);
        #         ol.translate3((cos(lux.time/2.0), cos(lux.time/3.0), cos(lux.time/7.0)))
        #         ol.rotate3Z(lux.time * pi * 0.1 * lux.TouchCubes_simple_rate)
        #         ol.rotate3X(lux.time * pi * 0.25 * lux.TouchCubes_simple_rate)
        #         ol.rotate3Y(lux.time * pi * 0.13 * lux.TouchCubes_simple_rate)
        #     else:
        #         ol.color3(0.0,1.0,1.0);
        #         ol.scale3((0.6, 0.6, 0.6))
        #         ol.translate3((cos(lux.time/3.2), cos(lux.time/2.6), cos(lux.time/5.4)))
        #         ol.rotate3Z(lux.time * pi * 0.14 * lux.TouchCubes_simple_rate)
        #         ol.rotate3X(lux.time * pi * 0.53 * lux.TouchCubes_simple_rate)
        #         ol.rotate3Y(lux.time * pi * 0.22 * lux.TouchCubes_simple_rate)
            
        #     ol.begin(ol.LINESTRIP)
        #     ol.vertex3((-1, -1, -1))
        #     ol.vertex3(( 1, -1, -1))
        #     ol.vertex3(( 1,  1, -1))
        #     ol.vertex3((-1,  1, -1))
        #     ol.vertex3((-1, -1, -1))
        #     ol.vertex3((-1, -1,  1))
        #     ol.end()

        #     ol.begin(ol.LINESTRIP);
        #     ol.vertex3(( 1,  1,  1))
        #     ol.vertex3((-1,  1,  1))
        #     ol.vertex3((-1, -1,  1))
        #     ol.vertex3(( 1, -1,  1))
        #     ol.vertex3(( 1,  1,  1))
        #     ol.vertex3(( 1,  1, -1))
        #     ol.end()

        #     ol.begin(ol.LINESTRIP)
        #     ol.vertex3(( 1, -1, -1))
        #     ol.vertex3(( 1, -1,  1))
        #     ol.end()

        #     ol.begin(ol.LINESTRIP)
        #     ol.vertex3((-1,  1,  1))
        #     ol.vertex3((-1,  1, -1))
        #     ol.end()
