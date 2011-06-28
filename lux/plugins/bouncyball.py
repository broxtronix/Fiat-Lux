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
    interval = .120
    nextSnapshot = 0
    samples = 512
    skip = 1
    renderPointCount = int(ceil(samples/skip))
    restRadius = .6
    currentWave = zeros(shape=(renderPointCount))
    nextWave = zeros(shape=(renderPointCount))

    # Constructor
    def __init__(self):
        pass
        
    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity()

        # Grab the raw audio buffers
        mono = audio_engine.mono_buffer()

        # Make sure they aren't empty!!
        if (mono.shape[0] == 0):
            return

        # Openlase can only draw 30000 points in one cycle (less that
        # that, actually!).  Clear the audio buffer and try again!
        if mono.shape[0] > 10000:
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
            for i in range(self.renderPointCount):
                self.nextWave[i] = mono[i*self.skip]
                    
        # draw shape
        fracIntervalComplete = (lux.time - (self.nextSnapshot - self.interval)) / self.interval
        #        print '%f %f %f' % (lux.time,fracIntervalComplete, self.nextSnapshot)
        coordsToRender = zeros(shape=(self.renderPointCount,2))
        firstVal = None
        for i in range(self.renderPointCount):
            val = ((self.nextWave[i] - self.currentWave[i]) * fracIntervalComplete) + self.currentWave[i]
            if (firstVal is None): firstVal = val
            #print "next: %f  curr:  %f   frac: %f" % (self.nextWave[i], self.currentWave[i], fracIntervalComplete)
            (x,y) = self.doTheTrigStuff(val, (float(i)/float(self.renderPointCount)), firstVal)
            coordsToRender[i][0] = x;
            coordsToRender[i][1] = y
        coordsToRender[self.renderPointCount-1] = coordsToRender[0]

        # render shape
        ol.begin(ol.POINTS)
        for i in range(self.renderPointCount):
#            print '%f: %f,%f' % (i,coordsToRender[i][0], coordsToRender[i][1])
            ol.vertex((coordsToRender[i][0], coordsToRender[i][1]))
        for i in range(3):  # Close the gap
            ol.vertex((coordsToRender[i][0], coordsToRender[i][1]))
        ol.end()
        
    def doTheTrigStuff(self, val, fracCircleComplete=1.0, smudgeVal=None):
        multipler = 1.0
        if (val > 0):
            # we are expanding
            multiplier = self.restRadius * 1.5
        else:
            # we are contracting
            multiplier = self.restRadius - .5
        
        # bias
        smudge = .2 # modify this to change how much room the smudge has
        if ((fracCircleComplete > (1.0 - smudge)) and (smudgeVal is not None)):
            fracSmudge = (fracCircleComplete - (1.0 - smudge)) / smudge
            oldval = val
            val = val + ((smudgeVal - val) * fracSmudge)
        
        hLen = (val * multipler) + self.restRadius
                
        x = cos(2 * pi * fracCircleComplete) * hLen
        y = sin(2 * pi * fracCircleComplete) * hLen
        
        # ensure we dont give out-of-bounds values
        if (x>1):x=1
        if (x<-1):x=-1
        if (y>1):y=1
        if (y<-1):y=-1
        
        #print "%f, %f, %f, %d: %f,%f" % (val, fracCircleComplete, hLen, multipler, x, y)
        return (x,y)
