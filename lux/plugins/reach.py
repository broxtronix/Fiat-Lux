"""
 * Reach 2.
 * Based on code from Keith Peters (www.bit-101.com).
 *
 * The arm follows the position of the mouse by
 * calculating the angles with atan2().
 *
 Ported from processing (http://processing.org/) examples.
"""
from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
import math
from math import pi
import random

SEGMENT_LENGTH = 0.025

class Segment():
    def __init__(self, x, y, width):
        self.x, self.y = x, y
        self.width = width

    def draw(self):
        ol.translate3(self.x, self.y, 0)
        ol.rotate3Z(self.angle)
        ol.begin(ol.LINESTRIP)
        ol.vertex3((0,0,0))
        ol.vertex3((SEGMENT_LENGTH, 0, 0))
        ol.end()

        #self.graphics.move_to(0, 0)
        #self.graphics.line_to(SEGMENT_LENGTH, 0)
        #self.graphics.set_color("#999")
        #self.graphics.set_line_style(width = width)
        #self.graphics.stroke()


class Arm():
    def __init__(self):
        self.segments = []
        parts = 20
        for i in range(parts):
            segment = Segment(0, 0, i)
            self.segments.append(segment)

    def draw(self, target):
        x, y =target[0], target[1]

        def get_angle(segment, x, y):
            return math.atan2(dy, dx)

        # point each segment to it's predecessor
        for segment in self.segments:
            dx = x - segment.x
            dy = y - segment.y
            angle = math.atan2(dy, dx)
            segment.angle = angle
            segment.rotation = angle

            x = x - math.cos(angle) * SEGMENT_LENGTH
            y = y - math.sin(angle) * SEGMENT_LENGTH

        # and now move the pointed nodes, starting from the last one
        # (that is the beginning of the arm)
        for prev, segment in reversed(list(zip(self.segments, self.segments[1:]))):
            prev.x = segment.x + math.cos(segment.angle) * SEGMENT_LENGTH
            prev.y = segment.y + math.sin(segment.angle) * SEGMENT_LENGTH

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
        target = [math.sin(2*pi*lux.time*3), math.sin(2*pi*lux.time*5)]
        self.arm.draw(target)

        ol.begin(ol.LINESTRIP)
        ol.vertex3((-1,  1,  1))
        ol.vertex3((-1,  1, -1))
        ol.end()


