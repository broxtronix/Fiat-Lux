#!/usr/bin/env python
# - coding: utf-8 -
# Copyright (C) 2010 Toms Bauģis <toms.baugis at gmail.com>

from __future__ import division
from hamster import pytweener
import random, math

from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import pi

draw_links = False

class Particle:
  def __init__(self, x=0, y=0, color=(1,1,0), follow=None):
    self.x = x
    self.y = y
    self.moving = False
    self.color=color
    self.follow=follow

  def __repr__(self):
    return "Particle(%.02f, %.02f)" % (self.x, self.y)
  
  def __setattr__(self, name, val):
    self.__dict__[name] = val
  
  def draw(self, val):
    '''a square'''
    ol.loadIdentity3()
    ol.loadIdentity()
    ol.color3(self.color[0], self.color[1], self.color[2])
    ol.translate3((self.x, self.y, 0))
    ol.begin(ol.POINTS)
    ol.vertex3((.0,.0,.0))
    ol.vertex3((.0,.1,.0))
    ol.vertex3((.1,.1,.0))
    ol.vertex3((.1,.0,.0))
    ol.vertex3((.0,.0,.0))
    ol.end()

    self.moving = True
    return self
  
  def finish(self, val):
    self.moving = False
    return self

class Chain:
  def __init__(self, tweener):
    self.tweener = tweener
    self.tail = []
    parts = 20
    for i in range(parts):
        previous = self.tail[-1] if self.tail else None
        #color = colorsys.hls_to_rgb(0.6, i / float(parts), 1)
        val = (parts - i)/parts
        color = (val, val, val)

        self.tail.append(Particle(0, 0, color, previous))

    #for tail in reversed(self.tail):
    #    self.add_child(tail) # add them to scene other way round
  
  def draw(self, target = None):
    for particle in reversed(self.tail):
        # draw connecting lines
        if particle.follow:
            new_x, new_y = particle.follow.x, particle.follow.y
            if draw_links:
                ol.color3(1,0,1) # magenta links
                ol.loadIdentity3()
                ol.loadIdentity()
                ol.begin(ol.LINESTRIP)
                ol.vertex3((particle.x, particle.y, 0))
                ol.vertex3((particle.follow.x, particle.follow.y, 0))
                ol.end()
        else:
            if target: new_x, new_y = target[0], target[1]
            else: new_x, new_y = math.cos(3*lux.time), math.sin(2*lux.time)
            #new_x, new_y = self.mouse_x, self.mouse_y
        particle.draw('blah')

        if abs(particle.x - new_x) > 0.01 or abs(particle.y - new_y) > 0.01:
            self.tweener.add_tween(particle, x=new_x, y=new_y, duration=0.9, \
                easing=pytweener.Easing.Cubic.ease_out, on_complete=particle.finish, on_update=particle.draw)
            
            #self.animate(particle, x = new_x, y = new_y, duration = 0.3, easing = Easing.Cubic.ease_out)

    # i dunno what this is about
    #if abs(self.tail[0].x - self.tail[-1].x) + abs(self.tail[0].y - self.tail[-1].y) > 1:
    #    self.redraw() # redraw if the tail is not on the head




class SimplePlugin(LuxPlugin):
    name = "Tween Chain"
    description = """
    easing animation test
    """
    def __init__(self):

        # This is how you register a parameter with the lux engine.
        # Parameters can be controlled using OSC or in the GUI.
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))
        self.tweener = pytweener.Tweener()
        self.chain = Chain(self.tweener)
        self.particle = Particle()
        self.last_time = 0
    def bounce(self):
        '''move the yellow square to a new location'''
        self.tweener.add_tween(self.particle, x=random.uniform(-1,1), y=random.uniform(-1,1), duration=0.3, \
          easing=pytweener.Easing.Bounce.ease_out, on_complete=self.particle.finish, on_update=self.particle.draw)

    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()
        
        if not self.particle.moving:
          self.bounce()

        self.chain.draw(target=(self.particle.x, self.particle.y))
        foo= self.tweener.update(lux.time - self.last_time)
        
        #print list(foo)
        #bar = list(foo)[0]

        ol.color3(1.0, 1.0, 1.0);
        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))

        self.last_time = lux.time

