#!/usr/bin/env python
# - coding: utf-8 -
# Copyright (C) 2010 Toms Bauģis <toms.baugis at gmail.com>

from __future__ import division
from hamster import pytweener
import random, math
import yaml

from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import pi

clamp_display = False

#parameters
#----------
scale = 1.5
time_scale = 1
bpm = 60
pulse_radius = True
pulse_angle = False
pulse_distance = False
pulse_color = True
node_small_radius = 0.01
node_big_radius = 0.03

max_nodes = 20
pulse_attack = 0.2
pulse_decay = 0.9
throb_propagation_speed = 200

ctf = 1/10  #color time frequency
clf = 0 #3/240 #color length frequncy
caf = 0.5  #color angle frequency
r_prime = 3
g_prime = 2
b_prime = 1
seizure_mode = True
#----------

#god this sucks
node_red = 1
node_green = 0.0
node_blue = 0.0

node_red_on = 0
node_green_on = 1
node_blue_on = 1

class Tweenable:
  def __setattr__(self, name, val):
    self.__dict__[name] = val

class Node(Tweenable):
    def __init__(self, angle, distance):
        self.angle = angle
        self.distance = distance
        self.base_angle = 0
        self.distance_scale = 1
        self.radius = node_small_radius
        self.phase = 0
        self.x, self.y = 0, 0
        self.red = node_red
        self.green = node_green
        self.blue = node_blue 
        self.R = 0.25 # big steps
        self.R_frequency =  1/100
        self.r = 0.08 # little steps
        self.r_frequency = 1/370
        self.p = 0.5 # size of the ring
        self.p_frequency = 1/2000


    def draw(self):
        '''a square'''
        #self.x = math.cos(2*pi*rotate_frequency*lux.time + self.angle + self.base_angle) * self.distance * self.distance_scale
        #self.y = math.sin(2*pi*rotate_frequency*lux.time + self.angle + self.base_angle) * self.distance * self.distance_scale
        
        #stolen from guilloche
        time = lux.time * time_scale 
        R = math.sin(2*pi*self.R_frequency*time) * self.R + 0.0001
        r = math.sin(2*pi*self.r_frequency*time) * self.r + 0.0001
        p = math.sin(2*pi*self.p_frequency*time) * self.p + 0.0001
        self.x = (R + r) * math.cos(time) + (r + p) * math.cos((R+r)/r * time) 
        self.y = (R + r) * math.sin(time) + (r + p) * math.sin((R+r)/r * time) 
        
        #clamp to display area
        if clamp_display:
            if self.x > 1: self.x = 1
            if self.y > 1: self.y = 1
            if self.x < -1: self.x = -1
            if self.y < -1: self.y = -1
        self.x *= scale
        self.y *= scale
        #self.graphics.circle(0, 0, self.radius)
        ol.loadIdentity3()
        ol.loadIdentity()


        #ol.color3(self.color[0], self.color[1], self.color[2])
        ol.color3(self.red, self.green, self.blue)
        ol.translate3((self.x, self.y, 0))
        angle = math.atan2(self.y, self.x)/(2*pi)
        red   = abs(math.sin(2*pi*(r_prime/3+ctf*time+clf*self.n+caf*angle)))*self.red
        green = abs(math.sin(2*pi*(g_prime/3+ctf*time+clf*self.n+caf*angle)))*self.green
        blue =  abs(math.sin(2*pi*(b_prime/3+ctf*time+clf*self.n+caf*angle)))*self.blue
        if seizure_mode:
          red, green, blue = red/self.radius, green/self.radius, blue/self.radius
          red, green, blue = red*(self.radius/node_big_radius), green*(self.radius/node_big_radius), blue*(self.radius/node_big_radius)
        
        ol.color3(red, green, blue)
 
        #do squares have radii?
        s = self.radius
        ol.begin(ol.POINTS)
        ol.vertex3((-s, s,0))
        ol.vertex3((-s, s,0))
        ol.vertex3(( s, s,0))
        ol.vertex3(( s,-s,0))
        ol.vertex3((-s,-s,0))
        ol.end()


class Net(Tweenable):
    def __init__(self, tweener):
        self.nodes = []
        self.tick = 0
        self.phase = 0
        self.tweener = tweener

    def on_mouse_move(self, scene, event):
        '''useless for openlase but might come in handy'''
        if gtk.gdk.BUTTON1_MASK & event.state:
            # rotate and scale on mouse
            base_angle = math.pi * 2 * ((self.width / 2 - event.x) / self.width) / 3
            distance_scale = math.sqrt((self.width / 2 - event.x) ** 2 + (self.height / 2 - event.y) ** 2) \
                             / math.sqrt((self.width / 2) ** 2 + (self.height / 2) ** 2)

            for node in self.nodes:
                node.base_angle = base_angle
                node.distance_scale = distance_scale

    def draw(self):
        if len(self.nodes) < max_nodes:
            for i in range(max_nodes - len(self.nodes)):
                angle = random.random() * math.pi * 2
                #distance = random.uniform(0, 1)
                distance = i / max_nodes

                node = Node(angle, distance)
                node.phase = self.phase
                self.nodes.append(node)
                node.n = i
                node.R = node.R #* node.n/max_nodes #random.uniform(0, 1)
                node.r = node.r * node.n/max_nodes #random.uniform(0, 1)
                node.p = node.p * node.n/max_nodes #random.uniform(0, 1)
                #node.R_frequency = node.R_frequency * random.uniform(0, 1)
                #node.r_frequency = node.r_frequency * random.uniform(0, 1)
                #node.p_frequency = node.p_frequency * random.uniform(0, 1)

        if not self.tick:
            self.phase +=1
            #this is just a fancy timer i guess
            self.tweener.add_tween(self, tick=throb_propagation_speed, duration=60/bpm, \
                easing=pytweener.Easing.Expo.ease_in_out, on_complete=self.reset_tick)

        for node in self.nodes:
            if node.phase < self.phase and node.distance < self.tick:
                node.phase = self.phase
                self.tweener.kill_tweens(node)
                if pulse_radius and pulse_color: #how do i separate this?
                  self.tweener.add_tween(node, radius=node_big_radius, red=node_red_on,\
                  green=node_green_on, blue=node_blue_on, duration=pulse_attack, \
                    easing=pytweener.Easing.Expo.ease_in, on_complete=self.slide_back)
#                if pulse_color:
#                  self.tweener.add_tween(node, color=1, duration=pulse_attack, \
#                    easing=pytweener.Easing.Expo.ease_in, on_complete=self.slide_back)
            
            node.draw()


    def reset_tick(self, target):
        self.tick = 0

    def slide_back(self, node):
        if pulse_radius:
          self.tweener.add_tween(node, radius=node_small_radius, duration=pulse_decay, \
            red=node_red, green=node_green, blue=node_blue, \
            easing=pytweener.Easing.Expo.ease_out)
        #if pulse_color:
        #  self.tweener.add_tween(node, color=node_color, duration=0.9, \
        #    easing=pytweener.Easing.Expo.ease_out)
        


class SimplePlugin(LuxPlugin):
    name = "Pulse"
    description = """
    rippling wave through nodes
    """
    def __init__(self):

        # This is how you register a parameter with the lux engine.
        # Parameters can be controlled using OSC or in the GUI.
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))
        self.tweener = pytweener.Tweener()
        self.net = Net(self.tweener)
        self.last_time = 0

    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()
        
#        dt = lux.time - self.last_time

        self.net.draw()
        foo= self.tweener.update(lux.time*time_scale - self.last_time)
        
        #print list(foo)
        #bar = list(foo)[0]

        ol.color3(1.0, 1.0, 1.0);
        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))

        self.last_time = lux.time * time_scale


