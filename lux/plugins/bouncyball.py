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
    nextSnapshot = 0
    samples = 512
    skip = 1
    renderPointCount = ceil(samples/skip)
    restRadius = .6
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
        
        if (lux.time > self.nextSnapshot):
            #print "snapshot"
            self.nextSnapshot = lux.time + self.interval
            self.currentWave = self.nextWave
            self.nextWave = zeros(shape=(self.renderPointCount))
            # load in new values
            for i in range(self.renderPointCount-1):
                self.nextWave[i] = (left[i*self.skip] + right[i*self.skip]) / 2
                    
        # draw shape
        fracIntervalComplete = (lux.time - (self.nextSnapshot - self.interval)) / self.interval
#        print '%f %f %f' % (lux.time,fracIntervalComplete, self.nextSnapshot)
        coordsToRender = zeros(shape=(self.renderPointCount,2))
        for i in range(self.renderPointCount-1):
            val = ((self.nextWave[i] - self.currentWave[i]) * fracIntervalComplete) + self.currentWave[i]
            #print "next: %f  curr:  %f   frac: %f" % (self.nextWave[i], self.currentWave[i], fracIntervalComplete)
            (x,y) = self.doTheTrigStuff(val, (float(i)/float(self.renderPointCount)))
            coordsToRender[i][0] = x;
            coordsToRender[i][1] = y
        coordsToRender[self.renderPointCount-1] = coordsToRender[0]

        # render shape
        ol.begin(ol.LINESTRIP)
        for i in range(self.renderPointCount):
#            print '%f: %f,%f' % (i,coordsToRender[i][0], coordsToRender[i][1])
            ol.vertex((coordsToRender[i][0], coordsToRender[i][1]))
        ol.end()
        
    def doTheTrigStuff(self, val, fracCircleComplete=1):
        multipler = 1.0
        if (val > 0):
            # we are expanding
            multiplier = self.restRadius * 1.5
        else:
            # we are contracting
            multiplier = self.restRadius - .5
        
        hLen = (val * multipler) + self.restRadius
        x = cos(2 * pi * fracCircleComplete) * hLen
        y = sin(2 * pi * fracCircleComplete) * hLen
        #print "%f, %f, %f, %d: %f,%f" % (val, fracCircleComplete, hLen, multipler, x, y)
        return (x,y)
