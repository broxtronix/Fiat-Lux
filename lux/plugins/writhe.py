from lux_plugin import LuxPlugin, ColorDriftPlugin
import pylase as ol
from audio import audio_engine

from parameters import lux, Parameter
from numpy import *
import numpy as np
import colorsys
import random

class WrithePlugin(LuxPlugin, ColorDriftPlugin):

    # Plugin Name
    name  =  "Writhe"

    # Plugin Description
    description  =  """
    self.BY Tristan Ursell
    """

    # Constructor
    def __init__(self):
        LuxPlugin.__init__(self)
        ColorDriftPlugin.__init__(self)

        # Number of points in cache
        self.N = 250
        self.scale_factor = 0.8
        self.ROT_RATE = 0.1

        # Color changing
        self.writhe_current_hue = random.random()
        self.writhe_hue_target = random.random()
        self.writhe_hue_step = 1.0/10.0
        
        #diffuse D-angle
        self.thetad = 0.2
        
        #seed angle   
        self.thetaB = random.random()*2*pi
        self.thetaR = random.random()*2*pi
        self.thetaG = random.random()*2*pi

        #seed position
        self.BX = arange(0.0,1.0,1.0/self.N)
        self.BY = arange(0.0,1.0,1.0/self.N)
        self.BX[0] = 0
        self.BY[0] = 0
        self.fB = 1.0

        self.RX=arange(0.0,1.0,1.0/self.N) 
        self.RY=arange(0.0,1.0,1.0/self.N)
        self.RX[0]=0
        self.RY[0]=0
        self.fR=1.0
       
        self.GX=arange(0,1.0,1.0/self.N)
        self.GY=arange(0,1.0,1.0/self.N)
        self.GX[0]=0
        self.GY[0]=0
        self.fG=1.0

        #jump distance
        self.dr=2.0/self.N;
       
        for i in range(1,self.N):
            self.thetaB=random.gauss(0,self.thetad)+self.thetaB;
            self.BX[i]=self.BX[i-1]+self.dr*cos(self.thetaB)
            self.BY[i]=self.BY[i-1]+self.dr*sin(self.thetaB)
    
            self.thetaR=random.gauss(0,self.thetad)+self.thetaR;
            self.RX[i]=self.RX[i-1]+self.dr*cos(self.thetaR)
            self.RY[i]=self.RY[i-1]+self.dr*sin(self.thetaR)
            
            self.thetaG=random.gauss(0,self.thetad)+self.thetaG;
            self.GX[i]=self.GX[i-1]+self.dr*cos(self.thetaG)
            self.GY[i]=self.GY[i-1]+self.dr*sin(self.thetaG)

        # loop variable
        self.i=1.0;

    # Slow, random evolution of hue. 
    def writhe_color_cycle(self):
        if (abs(self.writhe_hue_target - self.writhe_current_hue) < self.writhe_hue_step):
            self.writhe_hue_target = random.random()
        
        if (self.writhe_hue_target > self.writhe_current_hue):
            self.writhe_current_hue = self.writhe_current_hue + self.writhe_hue_step
        else:
            self.writhe_current_hue = self.writhe_current_hue - self.writhe_hue_step
            
        return colorsys.hsv_to_rgb(self.writhe_current_hue, 1.0, 1.0)

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 50000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/1.0
        params.off_speed = 1.0/1.0
        params.start_dwell = 0
        params.end_dwell = 0
        params.corner_dwell = 0
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 28
        params.end_wait = 95
        params.snap = 1/100000.0;
        params.render_flags = ol.RENDER_NOREORDER;
        ol.setRenderParams(params)

    # The draw method gets called roughly 30 times a second.
    def draw(self):
   
        self.i=self.i+1.0;
        
        #inverse persistence length
        self.thetad=0.25*(1.0+sin(2.0*pi*self.i/2000.0))
    
        #RGB curliness offset
        offset=pi/6.0
    
        #RGB curly-straight cycle frequency
        crlstrt=0.005
    
        #RGB maximum curlyness
        curlmx=0.2
    
        theta0B=curlmx*cos(self.i*crlstrt)
        theta0R=curlmx*cos(self.i*crlstrt+offset)
        theta0G=curlmx*cos(self.i*crlstrt+2.0*offset)
    
        self.thetaB=self.thetaB+random.gauss(theta0B,self.thetad)
        self.thetaR=self.thetaR+random.gauss(theta0R,self.thetad)
        self.thetaG=self.thetaG+random.gauss(theta0G,self.thetad)
    
        self.BX=np.append(self.BX[1:], self.BX[-1]+self.dr*cos(self.thetaB))
        self.BY=np.append(self.BY[1:], self.BY[-1]+self.dr*sin(self.thetaB))
        
        self.RX=np.append(self.RX[1:], self.RX[-1]+self.dr*cos(self.thetaR))
        self.RY=np.append(self.RY[1:], self.RY[-1]+self.dr*sin(self.thetaR))
    
        self.GX=np.append(self.GX[1:], self.GX[-1]+self.dr*cos(self.thetaG))
        self.GY=np.append(self.GY[1:], self.GY[-1]+self.dr*sin(self.thetaG))
         
        # derivative roughness parameter
        # b=0.1;
        # if b != 0.0:
        #     [Fx,Fy]=gradient([self.BX;self.RX;self.GX;self.BY;self.RY;self.GY])
        
        #     self.BX=b*Fx(4,:)+self.BX
        #     self.RX=b*Fx(5,:)+self.RX
        #     self.GX=b*Fx(6,:)+self.GX
        
        #     self.BY=b*Fx(1,:)+self.BY
        #     self.RY=b*Fx(2,:)+self.RY
        #     self.GY=b*Fx(3,:)+self.GY
    
        #combine paths
        rmult=0.0001;
        if 1:
            fmB=0.5
            fmG=0.5
        
            #            self.BX=(self.BX+self.RX+(2*random.uniform(1,self.N)-1.0)*rmult)/2.0
            self.BX=(self.BX+self.RX)/2.0
            self.BY=(self.BY+self.RY+(2*random.uniform(1,self.N)-1.0)*rmult)/2.0
        
            self.RX=(self.RX+self.GX+(2*random.uniform(1,self.N)-1.0)*rmult)/2.0
            self.RY=(self.RY+self.GY+(2*random.uniform(1,self.N)-1.0)*rmult)/2.0
        
            self.GX=(self.BX+self.GX+(2*random.uniform(1,self.N)-1.0)*rmult)/2.0
            self.GY=(self.BY+self.GY+(2*random.uniform(1,self.N)-1.0)*rmult)/2.0
        else:
            fmB=1.0
            fmG=1.0
    
        #spin frequency
        freq=0.01+random.gauss(0,0.002)
    
        self.BX=cos(freq*fmB)*self.BX-sin(freq*fmB)*self.BY
        self.BY=sin(freq*fmB)*self.BX+cos(freq*fmB)*self.BY
    
        self.RX=cos(freq)*self.RX-sin(freq)*self.RY
        self.RY=sin(freq)*self.RX+cos(freq)*self.RY
        
        self.GX=cos(freq*fmG)*self.GX-sin(freq*fmG)*self.GY
        self.GY=sin(freq*fmG)*self.GX+cos(freq*fmG)*self.GY
    
        #centering
        self.BX=self.BX-self.BX.mean()
        self.BY=self.BY-self.BY.mean()
    
        self.RX=self.RX-self.RX.mean()
        self.RY=self.RY-self.RY.mean()
    
        self.GX=self.GX-self.GX.mean()
        self.GY=self.GY-self.GY.mean()
    
        #scaling and bouncy factor
        bounce=5.0
        self.fB  =  self.fB + ((self.fB+max(np.sqrt(self.BX**2+self.BY**2)))/2.0-self.fB)/bounce
        self.fR  =  self.fR + ((self.fR+max(np.sqrt(self.RX**2+self.RY**2)))/2.0-self.fR)/bounce
        self.fG  =  self.fG + ((self.fG+max(np.sqrt(self.GX**2+self.GY**2)))/2.0-self.fG)/bounce
    
        self.BX=self.BX/self.fB
        self.BY=self.BY/self.fB
    
        self.RX=self.RX/self.fR
        self.RY=self.RY/self.fR
        
        self.GX=self.GX/self.fG
        self.GY=self.GY/self.fG    
    
        ####################################
        #LUX RENDERING CODE
        ####################################

        ol.loadIdentity3()
        ol.loadIdentity()
        #        ol.color3(*(self.color_cycle()))
        ol.scale3((self.scale_factor,self.scale_factor,self.scale_factor))
        theta_rot = 0.4*cos(1.7 * lux.time * self.ROT_RATE) + 0.6*cos(0.7 * lux.time * self.ROT_RATE)
        ol.rotate3Z(theta_rot)


        render_type  =  ol.POINTS

        current_hue_marker = self.writhe_current_hue
        current_hue_target = self.writhe_hue_target
        current_hue_step = self.writhe_hue_step
        
#        ol.color3(0.0,0.0,1.0)
        ol.begin(ol.POINTS)
        for i in range(self.BX.shape[0]):
            ol.color3(*(self.writhe_color_cycle()))
            ol.vertex3((self.BX[i], self.BY[i], -1))
        ol.end()

        self.writhe_current_hue = current_hue_marker
        self.writhe_current_target = current_hue_target
        self.writhe_current_step = current_hue_step

        ol.begin(ol.POINTS)
        for i in range(self.BX.shape[0]):
            ol.color3(*(self.writhe_color_cycle()))
            ol.vertex3((-self.BX[i], self.BY[i], -1))
        ol.end()

        self.writhe_current_hue = current_hue_marker
        self.writhe_current_target = current_hue_target
        self.writhe_current_step = current_hue_step

        ol.begin(ol.POINTS)
        for i in range(self.BX.shape[0]):
            ol.color3(*(self.writhe_color_cycle()))
            ol.vertex3((self.BX[i], -self.BY[i], -1))
        ol.end()

        self.writhe_current_hue = current_hue_marker
        self.writhe_current_target = current_hue_target
        self.writhe_current_step = current_hue_step

        ol.begin(ol.POINTS)
        for i in range(self.BX.shape[0]):
            ol.color3(*(self.writhe_color_cycle()))
            ol.vertex3((-self.BX[i], -self.BY[i], -1))
        ol.end()

#        ol.color3(1.0,0.0,0.0)
#         ol.begin(ol.POINTS)
#         for i in range(self.RX.shape[0]):
#             ol.vertex3((self.RX[i], self.RY[i], -1))
#         ol.end()

#         ol.begin(ol.POINTS)
#         for i in range(self.RX.shape[0]):
#             ol.vertex3((-self.RX[i], self.RY[i], -1))
#         ol.end()

#         ol.begin(ol.POINTS)
#         for i in range(self.RX.shape[0]):
#             ol.vertex3((self.RX[i], -self.RY[i], -1))
#         ol.end()

#         ol.begin(ol.POINTS)
#         for i in range(self.RX.shape[0]):
#             ol.vertex3((-self.RX[i], -self.RY[i], -1))
#         ol.end()

# #        ol.color3(0.0,1.0,0.0)
#         ol.begin(ol.POINTS)
#         for i in range(self.GX.shape[0]):
#             ol.vertex3((self.GX[i], self.GY[i], -1))
#         ol.end()

#         ol.begin(ol.POINTS)
#         for i in range(self.GX.shape[0]):
#             ol.vertex3((-self.GX[i], self.GY[i], -1))
#         ol.end()

#         ol.begin(ol.POINTS)
#         for i in range(self.GX.shape[0]):
#             ol.vertex3((self.GX[i], -self.GY[i], -1))
#         ol.end()

#         ol.begin(ol.POINTS)
#         for i in range(self.GX.shape[0]):
#             ol.vertex3((-self.GX[i], -self.GY[i], -1))
#         ol.end()
