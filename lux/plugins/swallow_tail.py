from lux_plugin import LuxPlugin, ColorDriftPlugin
import pylase as ol
from audio import audio_engine

from parameters import lux, Parameter
from numpy import *
import colorsys
import random

class SwallowTailPlugin(LuxPlugin, ColorDriftPlugin):

    # Plugin Name
    name = "Swallow Tail"

    # Plugin Description
    description = """
    By Tristan Ursell
    """

    # Constructor
    def __init__(self):
        LuxPlugin.__init__(self)
        ColorDriftPlugin.__init__(self)

        # Number of points in cache
        self.N = 250.0;

        # fixed dtheta
        self.dtheta=0.04;

        # switch cut off
        self.cut=0.7;
        #        self.cut=1.0;

        # magnitudes
        self.m1=0.1;
        self.m2=0.7;
        self.m3=0.4;
        self.m4=0.23;
        self.m5=0.11;
        # self.m1=0.8;
        # self.m2=0.4;
        # self.m3=0.2;
        # self.m4=0.1;
        # self.m5=0.1;


        # combo powers
        self.p1x=1.0/2.0;
        self.p1y=3.0/2.0;
        self.p2x=3.0/2.0;
        self.p2y=1.0/2.0;
        
        # coefficients
        self.th1=random.random()*2*pi;
        self.th2=random.random()*2*pi;
        self.th3=random.random()*2*pi;
        self.th4=random.random()*2*pi;
        self.th5=random.random()*2*pi;

        self.th1b=random.random()*2*pi;
        self.th2b=random.random()*2*pi;
        self.th3b=random.random()*2*pi;
        self.th4b=random.random()*2*pi;
        self.th5b=random.random()*2*pi;

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        theta = arange(0,2*pi,2*pi/self.N);

        # rotations in q-space
        mu = 0.01
        std=0.001;
        
        dth1=random.gauss(mu,std);
        dth2=random.gauss(mu,std);
        dth3=random.gauss(mu,std);
        dth4=random.gauss(mu,std);
        dth5=random.gauss(mu,std);
    
        dth1b=random.gauss(mu,std);
        dth2b=random.gauss(mu,std);
        dth3b=random.gauss(mu,std);
        dth4b=random.gauss(mu,std);
        dth5b=random.gauss(mu,std);
    
        # dth1=self.dtheta*(1-2*(random.random()<self.cut));
        # dth2=self.dtheta*(1-2*(random.random()<self.cut));
        # dth3=self.dtheta*(1-2*(random.random()<self.cut));
        # dth4=self.dtheta*(1-2*(random.random()<self.cut));
        # dth5=self.dtheta*(1-2*(random.random()<self.cut));
    
        # dth1b=self.dtheta*(1-2*(random.random()<self.cut));
        # dth2b=self.dtheta*(1-2*(random.random()<self.cut));
        # dth3b=self.dtheta*(1-2*(random.random()<self.cut));
        # dth4b=self.dtheta*(1-2*(random.random()<self.cut));
        # dth5b=self.dtheta*(1-2*(random.random()<self.cut));

        self.th1=self.th1+dth1;
        self.th2=self.th2+dth2;
        self.th3=self.th3+dth3;
        self.th4=self.th4+dth4;
        self.th5=self.th5+dth5;
    
        self.th1b=self.th1b+dth1b;
        self.th2b=self.th2b+dth2b;
        self.th3b=self.th3b+dth3b;
        self.th4b=self.th4b+dth4b;
        self.th5b=self.th5b+dth5b;
    
        c1=self.m1*cos(self.th1);
        s1=self.m1*sin(self.th1);
        c2=self.m2*cos(self.th2);
        s2=self.m2*sin(self.th2);
        c3=self.m3*cos(self.th3);
        s3=self.m3*sin(self.th3);
        c4=self.m4*cos(self.th4);
        s4=self.m4*sin(self.th4);
        c5=self.m5*cos(self.th5);
        s5=self.m5*sin(self.th5);
    
        X=c1*cos(theta+self.th1b)+c2*cos(2*theta+self.th2b)+c3*cos(3*theta+self.th3b)+c4*cos(4*theta+self.th4b)+c5*cos(5*theta+self.th5b);
        Y=s1*sin(theta+self.th1b)+s2*sin(2*theta+self.th2b)+s3*sin(3*theta+self.th3b)+s4*sin(4*theta+self.th4b)+s5*sin(5*theta+self.th5b);
    
        X=(X-X.mean()).astype("complex")
        Y=(Y-Y.mean()).astype("complex")

        s = arange(1,self.N+1,1)

        Xtemp=X**self.p1x * Y**self.p1y + 2*s*1j - self.N*1j;
        Ytemp=X**self.p2x * Y**self.p2y + 2*s*1j - self.N*1j;

        X=Xtemp.real
        Y=Ytemp.real

        X=tanh(2*X);
        Y=tanh(2*Y);

        ol.loadIdentity3()
        ol.loadIdentity()
        ol.color3(*(self.color_cycle()))

        render_type = ol.POINTS

        ol.begin(ol.POINTS)
        for i in range(X.shape[0]):
            ol.vertex3((X[i], Y[i], -1))
        ol.vertex3((X[0], Y[0], -1))
        ol.end()
        
        ol.begin(ol.POINTS)
        for i in range(X.shape[0]):
            ol.vertex3((-X[i], Y[i], -1))
        ol.vertex3((-X[0], Y[0], -1))
        ol.end()

        ol.begin(ol.POINTS)
        for i in range(X.shape[0]):
            ol.vertex3((0.7*X[i], -0.7*Y[i], -1))
        ol.vertex3((0.7*X[0], -0.7*Y[0], -1))
        ol.end()
        
        ol.begin(ol.POINTS)
        for i in range(X.shape[0]):
            ol.vertex3((-0.7*X[i], -0.7*Y[i], -1))
        ol.vertex3((-0.7*X[0], -0.7*Y[0], -1))
        ol.end()

