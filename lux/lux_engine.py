from PyQt4 import QtCore, QtGui
import time

import pylase as ol
from math import pi


class LuxThread(QtCore.QThread):

    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def exit(self):
        print '\t--> Shutting down Lux Engine.'
        self.exiting = True
        self.wait()

    # Note: This is never called directly. It is called by Qt once the
    # thread environment has been set up.
    def run(self):

        # Initialize OpenLase
        if (ol.init() != 0):
            raise Exception("Could not initialize openlase")
        time.sleep(2)
        ftime = 0
        frames = 0

        print '\t--> Starting up LUX Engine.'

        while not self.exiting:
            ol.loadIdentity3()
            ol.loadIdentity()

            font = ol.getDefaultFont()
            s = "Hi There!"
            w = ol.getStringWidth(font, 0.2, s)
            ol.drawString(font, (-w/2,0.1), 0.2, ol.C_WHITE, s)

            ol.perspective(60, 1, 1, 100)
            ol.translate3((0, 0, -3))

            for i in range(2):

                if (i == 1):
                    ol.color3(1.0,0.0,0.0);
                else:
                    ol.color3(0.0,1.0,0.0);
                    
		ol.scale3((0.6, 0.6, 0.6))
		ol.rotate3Z(ftime * pi * 0.1)
		ol.rotate3X(ftime * pi * 0.8)
		ol.rotate3Y(ftime * pi * 0.73)
                
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
            #            print "Frame time: %f, FPS:%f"%(frame_render_time, frame_render_time/ftime)
            
        # Shut down OpenLase
        ol.shutdown()
