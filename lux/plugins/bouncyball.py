from lux_plugin import LuxPlugin
import pylase as ol
from audio import audio_engine

from parameters import lux, Parameter
from math import *
from numpy  import *

class BouncyBall(LuxPlugin):

    # Plugin Name
    name = "Bouncy Ball"

    # Plugin Description
    description = """
    Bouncy Ball plugin for rendering audio.
    """

    # Working vars
    interval = .100
    nextRecord = 0
    samples = 512
    skip = 10
    renderPointCount = ceil(samples/skip)
    minDiameter = .5
    maxDiameter = 1.0
    currentWave = zeros(shape=(renderPointCount))
    nextWave = zeros(shape=(renderPointCount))

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

        # Grab the raw audio buffers
        left = audio_engine.left_buffer()
        right = audio_engine.right_buffer()
        mono = audio_engine.mono_buffer()

        # Make sure they aren't empty!!
        if (mono.shape[0] == 0 or left.shape[0] == 0 or right.shape[0] == 0):
            return

        # Openlase can only draw 30000 points in one cycle (less that
        # that, actually!).  Clear the audio buffer and try again!
        if left.shape[0] > 10000:
            audio_engine.clear_all()
            return

        if left.shape[0] != right.shape[0]:
            audio_engine.clear_all()
            return
        
        ol.color3(1.0,1.0,1.0)
        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))
        
        if (lux.time > self.nextRecord):
            print "snapshot"
            self.nextRecord = lux.time + self.interval
            self.currentWave = self.nextWave
            # load in new values
            for i in range(self.renderPointCount-1):
                self.nextWave[i] = left[i*self.skip]
                    
        # draw shape
        fracIntervalComplete = (lux.time - (self.nextRecord - self.interval)) / self.interval
        print '%f %f %f' % (lux.time,fracIntervalComplete, self.nextRecord)
        coordsToRender = zeros(shape=(self.renderPointCount,2))
        for i in range(self.renderPointCount-1):
            val = ((self.nextWave[i] - self.currentWave[i]) * fracIntervalComplete) + self.currentWave[i]
            (x,y) = self.doTheTrigStuff(val, (float(i)/float(self.renderPointCount)))
            coordsToRender[i][0] = x;
            coordsToRender[i][1] = y
        coordsToRender[self.renderPointCount-1] = coordsToRender[0]

        # render shape
        ol.begin(ol.LINESTRIP)
        for i in range(self.renderPointCount):
#            print '%f: %f,%f' % (i,coordsToRender[i][0], coordsToRender[i][1])
#            ol.vertex((1,1))
            ol.vertex((coordsToRender[i][0], coordsToRender[i][1]))
        ol.end()
        
    def doTheTrigStuff(self, val, fracCircleComplete=1):
        hLen = (val * (self.maxDiameter - self.minDiameter)) + self.minDiameter
        x = cos(2 * pi * fracCircleComplete) * hLen
        y = sin(2 * pi * fracCircleComplete) * hLen
#        print "%f, %f, %f: %f,%f" % (val, fracComplete, hLen, x, y)
        return (x,y)
