"""
 * Reach 2.
 * Based on code from Keith Peters (www.bit-101.com).
 *
 * The arm follows the position of the mouse by
 * calculating the angles with atan2().
 *
 Ported from processing (http://processing.org/) examples.
"""
from __future__ import division
from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
import math
from math import pi
import random

#SEGMENT_LENGTH = 0.025
arm_length = 1.5
swoosh_frequency = 1/5
parts = 20

class Segment():
    def __init__(self, x, y, width):
        self.x, self.y = x, y
        self.width = width
        self.previous = None

    def draw(self):
        ol.begin(ol.LINESTRIP)
        try:
            ol.vertex3((self.prev_x,self.prev_y,0))
        except AttributeError:
            pass
        ol.vertex3((self.x, self.y, 0))
        ol.end()

class Arm():
    def __init__(self):
        self.x, self.y = -1, -1
        self.segments = []
        for i in range(parts):
            segment = Segment(0, 0, i)
            self.segments.append(segment)

    def draw(self, target):
        x, y =target[0]-self.x, target[1]-self.y

        def get_angle(segment, x, y):
            return math.atan2(dy, dx)

        # point each segment to it's predecessor
        for segment in self.segments:
            dx = x - segment.x
            dy = y - segment.y
            angle = math.atan2(dy, dx)
            segment.angle = angle
            segment.rotation = angle

            x = x - math.cos(angle) * arm_length/parts
            y = y - math.sin(angle) * arm_length/parts

        # and now move the pointed nodes, starting from the last one
        # (that is the beginning of the arm)
        for prev, segment in reversed(list(zip(self.segments, self.segments[1:]))):
            prev.x = segment.x + math.cos(segment.angle) * arm_length/parts
            prev.y = segment.y + math.sin(segment.angle) * arm_length/parts
            segment.prev_x = prev.x
            segment.prev_y = prev.y

        ol.translate3((self.x, self.y, 0))
        for segment in self.segments:
            segment.draw()

    def on_enter_frame(self, scene, context):
        self.segments[-1].y = self.height


class SimplePlugin(LuxPlugin):
    name = "reach"
    description = """
    dancing seaweed
    """
    def __init__(self):
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))
        self.arm = Arm()

    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()
        ol.color3(1.0, 0.0, 1.0);
        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))

        #target = [random.uniform(-1, 1), random.uniform(-1, 1)]
        #target_x, target_y = random.uniform(-1, 1), random.uniform(-1, 1)
        target_x, target_y = math.sin(2*pi*swoosh_frequency*lux.time*3), math.sin(2*pi*swoosh_frequency*lux.time*5)
        self.arm.draw([target_x, target_y])

        ol.begin(ol.LINESTRIP)
        ol.vertex3((-1,  1,  1))
        ol.vertex3((-1,  1, -1))
        ol.end()


