from PyQt4 import QtCore, QtGui
import time

import pylase as ol
from math import pi

from parameters import lux, Parameter
from plugins import LuxPlugin

class LuxEngine(QtCore.QThread):

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.current_plugin = 1

        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))


    def __del__(self):
        self.exiting = True
        self.wait()

    # Called by other threads.
    def exit(self):
        print '\t--> Shutting down Lux Engine.'
        self.exiting = True
        self.wait()

    # Note: This is never called directly. It is called by Qt once the
    # thread environment has been set up.
    def run(self):

        print lux.time

        # Initialize OpenLase
        if (ol.init() != 0):
            raise Exception("Could not initialize openlase")
        time.sleep(2)
        ftime = 0
        frames = 0
        print lux.time

        print '\t--> Starting up LUX Engine.'

        while not self.exiting:
            if (self.current_plugin):
                #                self.current_plugin.draw()
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

                frame_render_time = ol.renderFrame(60) # Takes max_fps as argument
                frames += 1
                ftime += frame_render_time
                #print "Frame time: %f, FPS:%f"%(frame_render_time, frame_render_time/ftime)
            else:
                time.sleep(0.1)
            
        # Shut down OpenLase
        ol.shutdown()
