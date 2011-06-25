from lux_plugin import LuxPlugin
import pylase as ol
from audio import audio_engine

from parameters import lux, Parameter
from math import *

from numpy import *

def obj_loader(filepath):
    obj_file = open(filepath)
   
    verts = []
    faces = []
    for line in obj_file:
        # Ignore comments and empty lines
        if line.strip() == "" or line.strip().startswith("#"):
            continue
        line_command = line.split()[0]
        if line_command == "v":
            verts.append([float(c) for c in line.split()[1:] ])
        if line_command == "f":
            faces.append([int(c.split("/")[0]) - 1 for c in line.split()[1:] ])
    return array(verts, dtype=float32), faces


class MeshViewer(LuxPlugin):
    # Plugin Name
    name = "Mesh Viewer"

    # Plugin Description
    description = """
    Step 1.) Load OBJ file
    Step 2.) Watch!
    """

    # Constructor
    def __init__(self):
        # This is how you register a parameter with the lux engine.
        # Parameters can be controlled using OSC or in the GUI.
        lux.register(Parameter( name = "simple_rate",
                                description = "0..1   controls the rate of spinning cubes",
                                default_value = 1.0 ))

        self.verts, self.faces = obj_loader("plugins/obj-files/shuttle.obj")
        print "Loaded %i vertices and %i faces" % (self.verts.shape[0], len(self.faces))
        self.loaded = False

        vmin = self.verts.min(axis=0)
        vmax = self.verts.max(axis=0)
        
        self.verts -= vmin
        self.verts /= vmax
        
        self.torender = arange(len(self.faces))

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        ol.loadIdentity3()
        ol.perspective(20, 1, 1, 100)
        ol.translate3((0, 0, -20))

        ol.color3(1.0,1.0,0.0);
        ol.translate3( (cos(lux.time/2.0), cos(lux.time/3.0), cos(lux.time/7.0)) )
        ol.rotate3Z(lux.time * pi * 0.1 * lux.simple_rate)
        ol.rotate3X(lux.time * pi * 0.25 * lux.simple_rate)
        ol.rotate3Y(lux.time * pi * 0.13 * lux.simple_rate)
        

        for row in self.torender:
            ol.begin(ol.LINESTRIP)
            vi = self.faces[row]
            vi = vi + [vi[0]]

            for i in vi:
                tup = tuple(self.verts[i,:])
                ol.vertex3(tup)
            
            ol.end()
