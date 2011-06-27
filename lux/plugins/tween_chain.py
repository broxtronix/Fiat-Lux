#!/usr/bin/env python
# - coding: utf-8 -
# Copyright (C) 2010 Toms Bauģis <toms.baugis at gmail.com>

from hamster import pytweener
import random

from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import pi

class Particle:
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y
    self.moving = False
  def __repr__(self):
    return "Particle(%02d, %02d)" % (self.x, self.y)
  def __setattr__(self, name, val):
#    if self.__dict__.get(name, "hamster_graphics_no_value_really") == val:
#      return
    self.__dict__[name] = val
  def draw(self, val):
    ol.translate3((self.x, self.y, 0))
    ol.begin(ol.LINESTRIP)
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
        self.particle = Particle()
        self.tweener = pytweener.Tweener()
    def bounce(self):
        self.tweener.add_tween(self.particle, x=random.uniform(-1,1), y=random.uniform(-1,1), duration=100.0, easing=pytweener.Easing.Bounce.ease_out, \
            on_complete=self.particle.finish, on_update=self.particle.draw)

    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()
        
        #if lux.time % 50 > 0 and not self.particle.moving:
        if not self.particle.moving:
          self.bounce()

        #if not self.particle.moving:
          #print 'hi!'
        foo= self.tweener.update(1)
        #print list( self.tweener.update(1))
        
        #print list(foo)
        #bar = list(foo)[0]

        ol.color3(1.0, 1.0, 1.0);
        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))


old_code='''

import colorsys

import gtk
from hamster import graphics
from hamster.pytweener import Easing
from math import floor


class TailParticle(graphics.Sprite):
    def __init__(self, x, y, color, follow = None):
        graphics.Sprite.__init__(self, x = x, y = y)
        self.follow = follow
        self.color = color
        self.add_child(graphics.Rectangle(20, 20, 3, color, x=-10, y=-10))
        self.graphics.fill(color)


class Canvas(graphics.Scene):
    def __init__(self):
        graphics.Scene.__init__(self)

        self.tail = []
        parts = 30
        for i in range(parts):
            previous = self.tail[-1] if self.tail else None
            color = colorsys.hls_to_rgb(0.6, i / float(parts), 1)

            self.tail.append(TailParticle(10, 10, color, previous))

        for tail in reversed(self.tail):
            self.add_child(tail) # add them to scene other way round


        self.mouse_moving = False

        self.connect("on-mouse-move", self.on_mouse_move)
        self.connect("on-enter-frame", self.on_enter_frame)


    def on_mouse_move(self, area, event):
        self.redraw()


    def on_enter_frame(self, scene, context):
        g = graphics.Graphics(context)
        for particle in reversed(self.tail):
            if particle.follow:
                new_x, new_y = particle.follow.x, particle.follow.y
                g.move_to(particle.x, particle.y)
                g.line_to(particle.follow.x, particle.follow.y)
                g.stroke(particle.color)
            else:
                new_x, new_y = self.mouse_x, self.mouse_y


            if abs(particle.x - new_x) + abs(particle.y - new_y) > 0.01:
                self.animate(particle, x = new_x, y = new_y, duration = 0.3, easing = Easing.Cubic.ease_out)


        if abs(self.tail[0].x - self.tail[-1].x) + abs(self.tail[0].y - self.tail[-1].y) > 1:
            self.redraw() # redraw if the tail is not on the head


class BasicWindow:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_default_size(500, 300)
        window.connect("delete_event", lambda *args: gtk.main_quit())

        canvas = Canvas()

        box = gtk.VBox()
        box.pack_start(canvas)


        window.add(box)
        window.show_all()


if __name__ == "__main__":
    example = BasicWindow()
    gtk.main()
'''
