from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine
from sprites import pytweener

import pylase as ol
from math import *
import random

# --------------- HARD-CODED PARAMETERS ----------------

PHOTON_SPEED = 0.05           # Number of seconds to get from one side to the other
PHOTON_RED = 0.0
PHOTON_GREEN = 0.0
PHOTON_BLUE = 1.0
PHOTON_SIZE = 0.01
MAX_PHOTONS = 100              # Max number of photons to have on screen at any given time
SPAWN_THRESHOLD = 0.10         # How likely on a scale of 0.0 to 1.0 is it that a photon will appear on a given frame.
CAVITY_SIZE = (3.0, 0.5)

# ---------------  UTILITY FUNCTIONS  ----------------

def square(x1,y1,x2,y2):
    
    ol.begin(ol.POINTS)
    ol.vertex3((x1,y1,0))
    ol.vertex3((x1,y2,0))
    ol.vertex3((x2,y2,0))        
    ol.vertex3((x2,y1,0))        
    ol.vertex3((x1,y1,0))  
    ol.end()

# ---------------    PHOTON CLASS   ----------------

class Photon(object):

    def __init__(self):
        self.reset()
        
    def draw(self):
        ol.color3(self.red,self.green,self.blue)
        square(self.x+PHOTON_SIZE, self.y+PHOTON_SIZE, self.x-PHOTON_SIZE, self.y-PHOTON_SIZE)

    def update(self, dt, photon_speed):
        new_x = self.x + cos(self.theta) * dt / photon_speed
        new_y = self.y + sin(self.theta) * dt / photon_speed

        # Case 1: Escaped photon
        if self.escaped:
            if self.x < 10.0:
                self.x = new_x
                self.y = new_y
                return
            else:
                self.reset()
                return

        # Case 2: Captured photon hits top wall.  Photon is lost!
        elif (new_y > CAVITY_SIZE[1]/2.0 or new_y < -CAVITY_SIZE[1]/2.0):
            self.reset()
            
        # Case 3: Captured photon hits left wall.  Reflect!
        elif (new_x < -CAVITY_SIZE[0]/2.0):
            self.theta = pi - self.theta + random.normalvariate(0,0.01)

        # Case 4: Captured photon hits right wall. Reflect or leave through aperture!
        elif (new_x > CAVITY_SIZE[0]/2.0):
            if new_y < 0.05 and new_y > -0.05:
                # Photon escapes
                self.escaped = True
                self.x = new_x
                self.y = new_y
            else:
                # Photon reflects
                self.theta = pi - self.theta + random.normalvariate(0,0.01)

        # Case 5: Photon is moving through cavity
        else:
            self.x = new_x
            self.y = new_y

    def reset(self):
        self.escaped = False
        self.x = (random.random() - 0.5) * CAVITY_SIZE[0]
        self.y = (random.random() - 0.5) * CAVITY_SIZE[1]
        if (random.random() > 0.5):
            self.theta = 0 + random.normalvariate(0,0.1)
        else:
            self.theta = pi
        self.red = PHOTON_RED
        self.green = PHOTON_GREEN
        self.blue = PHOTON_BLUE
        
# ---------------     PLUGIN CLASS     ----------------
class Tweenable:
  def __setattr__(self, name, val):
    self.__dict__[name] = val

class StimulatedEmissionPlugin(LuxPlugin, Tweenable):

    # Plugin Name
    name = "Stimulated Emission"

    # Plugin Description
    description = """
    This plugin is useful for describing the inner workings of a LASER to third graders.
    """

    def __init__(self):
        self.photons = []
        self.last_time = lux.time
        self.photon_speed = PHOTON_SPEED
        self.tweener = pytweener.Tweener()
        self.scale_factor = 0.4
        self.time_scale = 0.2

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 50000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/20.0
        params.off_speed = 1.0/14.0
        params.start_dwell = 0
        params.end_dwell = 8
        params.corner_dwell = 8
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 11
        params.end_wait = 0
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    def draw(self):
        self.tweener.add_tween(self, scale_factor=0.25, time_scale = 1.0, duration=0.1, \
                               easing=pytweener.Easing.Expo.ease_in_out)

        
        ol.loadIdentity()
        ol.loadIdentity3()
        ol.translate3((-0.1, 0.0, 0.0))
        ol.scale3((self.scale_factor, self.scale_factor, self.scale_factor))

        # Spawn photons randomly
        if len(self.photons) < MAX_PHOTONS and random.random() < SPAWN_THRESHOLD:
            p = Photon();
            self.photons.append(p)

        # Draw photons
        dt = self.time_scale * (lux.time - self.last_time)
        self.last_time = lux.time
        self.tweener.update(lux.time - self.last_time)
        
        for p in self.photons:
            p.update(dt, self.photon_speed)
            p.draw()

        ol.color3(1.0, 1.0, 1.0);
        font = ol.getDefaultFont()
        s = "LASER"
        w = ol.getStringWidth(font, 1.0, s)
        ol.drawString(font, (-w/2,1.1), 1.0, s)

        # Draw the bounding box, with a very small hole in it.
        ol.color3(0.0, 1.0, 0.0);
        ol.begin(ol.LINESTRIP)
        ol.vertex3(( CAVITY_SIZE[0]/2,  0.1, 0.0))
        ol.vertex3(( CAVITY_SIZE[0]/2,  CAVITY_SIZE[1]/2, 0.0))
        ol.vertex3((-CAVITY_SIZE[0]/2,  CAVITY_SIZE[1]/2, 0.0))
        ol.vertex3((-CAVITY_SIZE[0]/2, -CAVITY_SIZE[1]/2, 0.0))
        ol.vertex3(( CAVITY_SIZE[0]/2, -CAVITY_SIZE[1]/2, 0.0))
        ol.vertex3(( CAVITY_SIZE[0]/2,  -0.1, 0.0))
        ol.end()

        #ol.color3(1.0, 0.0, 0.0);
        #square(CAVITY_SIZE[0]/2-0.02, 0.15,CAVITY_SIZE[0]/2+0.02,0.05)
        #square(CAVITY_SIZE[0]/2-0.02, -0.15,CAVITY_SIZE[0]/2+0.02,-0.05)


    def reset(self):
        self.photons = []
        self.photon_speed = PHOTON_SPEED
        self.tweener.kill_tweens(self)
        self.scale_factor = 0.4
        self.time_scale = 0.2
