from lux_plugin import LuxPlugin
import pylase as ol
from audio import audio_engine

from parameters import lux, Parameter
from math import *

class Scope(LuxPlugin):

    # Plugin Name
    name = "Oscilloscope"

    # Plugin Description
    description = """
    Oscilloscope plugin for rendering audio.
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

        ol.loadIdentity3()
        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -5))

        ol.color3(1.0,0.0,1.0);

        ol.begin(ol.LINESTRIP)
        for i in range(left.shape[0]):
            pass
#            if (i % 10 == 0):
 #               ol.vertex3((left[i]*100, right[i]*100, -1))
        ol.end()
