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

draw_links = False

###parameters
bpm = 60
pulse_radius = True
pulse_angle = False
pulse_distance = False
pulse_color = True
node_small_radius = 0.01
node_big_radius = 0.1

max_nodes = 20
pulse_attack = 0.2
pulse_decay = 0.9

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

    def draw(self):
        '''a square'''
        self.x = math.cos(self.angle + self.base_angle) * self.distance * self.distance_scale
        self.y = math.sin(self.angle + self.base_angle) * self.distance * self.distance_scale

        #self.graphics.circle(0, 0, self.radius)
        ol.loadIdentity3()
        ol.loadIdentity()
        #ol.color3(self.color[0], self.color[1], self.color[2])
        ol.color3(self.red, self.green, self.blue)
        ol.translate3((self.x, self.y, 0))
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
                distance = random.uniform(0, 1)

                node = Node(angle, distance)
                node.phase = self.phase
                self.nodes.append(node)

        if not self.tick:
            self.phase +=1
            #this is just a fancy timer i guess
            self.tweener.add_tween(self, tick=550, duration=60/bpm, \
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
        foo= self.tweener.update(lux.time - self.last_time)
        
        #print list(foo)
        #bar = list(foo)[0]

        ol.color3(1.0, 1.0, 1.0);
        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))

        self.last_time = lux.time


