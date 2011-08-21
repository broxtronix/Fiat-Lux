from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import pi,cos,sin, exp

from random import randint, random
from time import sleep

import Image
import ImageOps

SIZEX,SIZEY = 200,200
lena = Image.open("/Users/levskaya/repos/Fiat-Lux/lux/plugins/lena.ppm").convert("L").crop((200,200,400,400)).resize((SIZEX,SIZEY))

#lena = Image.open("/Users/levskaya/phage.png").convert("L").resize((100,100))
#lena = ImageOps.invert(lena)

lenadat=[]
for i in range(SIZEX):
    for j in range(SIZEY):
        lenadat.append(lena.getpixel((i,j)))

rndidx=[]
rndtot=0
for i in range(SIZEX):
    for j in range(SIZEY):
        rndtot=rndtot+lena.getpixel((i,j))
        rndidx.append(rndtot)

def rndlena():
    rnd=randint(0,rndtot)
    for i in range(SIZEX):
        for j in range(SIZEY):
            if rndidx[i*SIZEX+j]>rnd:
                return (i,j,lena.getpixel((i,j)))
    
def square(posx,posy,size):
    ol.begin(ol.POINTS)
    #ol.begin(ol.LINESTRIP)
    ol.vertex3((posx,posy,0))
    ol.vertex3((posx+size,posy,0))
    ol.vertex3((posx+size,posy+size,0))
    ol.vertex3((posx,posy+size,0))
    ol.vertex3((posx,posy,0))
    ol.end()

class SimplePlugin(LuxPlugin):

    # Plugin Name
    name = "PhosphoPaint"

    # Plugin Description
    description = """
    Paints phosphor images
    """

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 50000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/28.0
        params.off_speed = 1.0/8.0
        params.start_dwell = 5
        params.end_dwell = 5
        params.corner_dwell = 20
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 24
        params.end_wait = 24
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    
    # Constructor
    def __init__(self):
        # This is how you register a parameter with the lux engine.
        # Parameters can be controlled using OSC or in the GUI.
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = .3 ))

        
    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        #set basic coord system
        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -40))

        ol.color3(0.0,0.0,1.0);
        ol.scale3((1., 1., 1.))

        #for i in range(10):
        #    x = random()*40-20
        #    y = random()*40-20
            #x = randint(-20,20)
            #y = randint(-20,20)
        #    square(x,y,.1)

        # truly randomly sampled by image vals
        #for i in range(20):
        #    x,y,val = rndlena()
        #    ol.color3(0.0,0.0,val/255.)
        #    square(x*40./SIZEX-20,y*40/SIZEY-20,.1)

        #totally random, weighted by image value
        for i in range(20):
            x=randint(0,SIZEX-1)
            y=randint(0,SIZEY-1)
            #val = lena.getpixel((x,y))        
            #val = 1.-exp(-.5*lenadat[x*SIZEX+y]/255.)
            val = lenadat[x*SIZEX+y]/255.*.77
            ol.color3(0.0,0.0,val)
            square(x*40./SIZEX-20,y*40/SIZEY-20,.05)


