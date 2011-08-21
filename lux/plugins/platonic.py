from lux_plugin import LuxPlugin
from parameters import lux, Parameter
from audio import audio_engine

import pylase as ol
from math import pi,cos,sin

class SimplePlugin(LuxPlugin):

    # Plugin Name
    name = "Platonic"

    # Plugin Description
    description = """
    It's just a platonic relationship.
    """

    # Custom parameters for the Fiat Lux lasers as tuned for Priceless
    def setParameters(self):
        params = ol.getRenderParams()
        params.rate = 50000
        #params.max_framelen = settings['calibration'].olRate
        params.on_speed = 1.0/28.0
        params.off_speed = 1.0/8.0
        params.start_dwell = 4
        params.end_dwell = 4
        params.corner_dwell = 10
        params.curve_dwell = 0
        params.curve_angle = cos(30.0*(pi/180.0)); # 30 deg
        params.start_wait = 1
        params.end_wait = 1
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

        tetrahedron_points=((0., 0., 0.612372),
                         (-0.288675, -0.5, -0.204124),
                         (-0.288675,  0.5, -0.204124),
                         (0.57735, 0., -0.204124))
        tetrahedron_faces=((2, 3, 4), (3, 2, 1), (4, 1, 2), (1, 4, 3))

        tetrahedron_strips=((1, 2, 3, 1), (1,4,3), (4, 2))
        self.tetrahedron_face_edges=[]
        for f in tetrahedron_strips:
            tmp=[]
            for s in f:
                tmp.append(tetrahedron_points[s-1])
            self.tetrahedron_face_edges.append( tmp )

        octahedron_points=((-0.707107, 0., 0.), (0., 0.707107, 0.), (0., 0., -0.707107),
              (0., 0., 0.707107), (0., -0.707107, 0.), (0.707107, 0., 0.))
        octahedron_faces=((4, 5, 6), (4, 6, 2), (4, 2, 1), (4, 1, 5),
                          (5, 1, 3), (5, 3, 6), (3, 1, 2), (6, 3, 2))
        octahedron_strips=((1,2,3),(1,4,5),(6,2,4),(6,3,5))
        
        self.octahedron_face_edges=[]
        for f in octahedron_strips:
            tmp=[]
            for s in f:
                tmp.append(octahedron_points[s-1])
            self.octahedron_face_edges.append( tmp )
            
        icos_points=((0.0, -0.52573099999999995, 0.85065100000000005),
                     (0.85065100000000005, 0.0, 0.52573099999999995),
                     (0.85065100000000005, 0.0, -0.52573099999999995),
                     (-0.85065100000000005, 0.0, -0.52573099999999995),
                     (-0.85065100000000005, 0.0, 0.52573099999999995),
                     (-0.52573099999999995, 0.85065100000000005, 0.0),
                     (0.52573099999999995, 0.85065100000000005, 0.0),
                     (0.52573099999999995, -0.85065100000000005, 0.0),
                     (-0.52573099999999995, -0.85065100000000005, 0.0),
                     (0.0, -0.52573099999999995, -0.85065100000000005),
                     (0.0, 0.52573099999999995, -0.85065100000000005),
                     (0.0, 0.52573099999999995, 0.85065100000000005))
        icos_faces=((1, 2, 6), (1, 7, 2), (3, 4, 5), (4, 3, 8), (6, 5, 11),
                    (5, 6, 10), (9, 10, 2), (10, 9, 3), (7, 8, 9), (8, 7, 0),
                    (11, 0, 1), (0, 11, 4), (6, 2, 10), (1, 6, 11), (3, 5, 10),
                    (5, 4, 11), (2, 7, 9), (7, 1, 0), (3, 9, 8), (4, 8, 0))
        icos_strips=((2, 12, 8, 7, 11, 4, 12, 10, 6, 5, 9, 1),
                     (2, 8, 3, 10, 1), (2, 7, 9, 3, 1), (2, 11, 5, 1), (2, 4, 6, 1),
                     (10, 8), (3, 7), (9, 11), (5, 4), (6, 12))
        self.icos_face_edges=[]
        for f in icos_faces:
            self.icos_face_edges.append( [icos_points[f[0]], icos_points[f[1]], icos_points[f[2]] ] )
        #for f in icos_strips:
        #    tmp=[]
        #    for s in f:
        #        tmp.append(icos_points[s-1])
        #    self.icos_face_edges.append( tmp )

        dodeca_points=((-1.37638, 0., 0.262866),
                       (1.37638, 0., -0.262866),
                       (-0.425325, -1.30902, 0.262866),
                       (-0.425325, 1.30902, 0.262866),
                       (1.11352, -0.809017, 0.262866),
                       (1.11352,  0.809017, 0.262866),
                       (-0.262866, -0.809017, 1.11352),
                       (-0.262866, 0.809017, 1.11352),
                       (-0.688191, -0.5, -1.11352),
                       (-0.688191,  0.5, -1.11352),
                       (0.688191, -0.5, 1.11352),
                       (0.688191, 0.5,  1.11352),
                       (0.850651, 0., -1.11352),
                       (-1.11352, -0.809017, -0.262866),
                       (-1.11352,  0.809017, -0.262866),
                       (-0.850651, 0., 1.11352),
                       (0.262866, -0.809017, -1.11352),
                       (0.262866,  0.809017, -1.11352),
                       (0.425325, -1.30902, -0.262866),
                       (0.425325,  1.30902, -0.262866))
        dodeca_faces=((15, 10, 9, 14, 1), (2, 6, 12, 11, 5), (5, 11, 7, 3, 19),
                     (11, 12, 8, 16, 7), (12, 6, 20, 4, 8), (6, 2, 13, 18, 20),
                     (2, 5, 19, 17, 13), (4, 20, 18, 10, 15), (18, 13, 17, 9, 10),
                     (17, 19, 3, 14, 9), (3, 7, 16, 1, 14), (16, 8, 4, 15, 1))
        self.dodeca_face_edges=[]
        for f in dodeca_faces:
            self.dodeca_face_edges.append( [dodeca_points[f[0]-1],
                                            dodeca_points[f[1]-1],
                                            dodeca_points[f[2]-1],
                                            dodeca_points[f[3]-1],
                                            dodeca_points[f[4]-1]] )

    # The draw method gets called roughly 30 times a second.  
    def draw(self):
        ol.loadIdentity3()
        ol.loadIdentity()

        #ol.color3(1.0, 0.0, 1.0);
        #font = ol.getDefaultFont()
        #s = "Lux!"
        #w = ol.getStringWidth(font, 0.2, s)
        #ol.drawString(font, (-w/2,0.1), 0.2, s)

        ol.perspective(60, 1, 1, 100)
        ol.translate3((0, 0, -3))


        #Dodecahedron---------------------------
        ol.color3(1.0,1.0,1.0);
        ol.scale3((0.8, 0.8, 0.8))
        ol.rotate3Z(lux.time * pi * 0.1 * lux.simple_rate)
        ol.rotate3X(lux.time * pi * 0.8 * lux.simple_rate)
        ol.rotate3Y(lux.time * pi * 0.73 * lux.simple_rate)

        for face in self.dodeca_face_edges:
            ol.begin(ol.LINESTRIP)
            ol.vertex3(face[0])
            ol.vertex3(face[1])
            ol.vertex3(face[2])
            ol.vertex3(face[3])
            ol.vertex3(face[4])
            ol.vertex3(face[0])
            ol.end()

        #Icosahedron---------------------------
        ol.color3(1.0,1.0,0.0);
                    
        ol.scale3((0.9, 0.9, 0.9))
        ol.rotate3Z(lux.time * pi * 0.5 * lux.simple_rate)
        #ol.rotate3X(lux.time * pi * 0.8 * lux.simple_rate)
        #ol.rotate3Y(lux.time * pi * 0.73 * lux.simple_rate)

        for face in self.icos_face_edges:
            ol.begin(ol.LINESTRIP)
            ol.vertex3(face[0])
            ol.vertex3(face[1])
            ol.vertex3(face[2])
            ol.vertex3(face[0])
            ol.end()
        #for strip in self.icos_face_edges:
        #    ol.begin(ol.LINESTRIP)
        #    for f in strip:
        #        ol.vertex3(f)
        #    ol.end()

        #Cube---------------------------
#         ol.color3(0.0,0.0,1.0);
#         ol.scale3((0.4, 0.4, 0.4))
#         #ol.rotate3Z(lux.time * pi * 0.1 * lux.simple_rate)
#         #ol.rotate3X(lux.time * pi * 0.8 * lux.simple_rate)
#         ol.rotate3Y(lux.time * pi * 0.73 * lux.simple_rate)

#         ol.begin(ol.LINESTRIP)
#         ol.vertex3((-1, -1, -1))
#         ol.vertex3(( 1, -1, -1))
#         ol.vertex3(( 1,  1, -1))
#         ol.vertex3((-1,  1, -1))
#         ol.vertex3((-1, -1, -1))
#         ol.vertex3((-1, -1,  1))
#         ol.end()
        
#         ol.begin(ol.LINESTRIP);
#         ol.vertex3(( 1,  1,  1))
#         ol.vertex3((-1,  1,  1))
#         ol.vertex3((-1, -1,  1))
#         ol.vertex3(( 1, -1,  1))
#         ol.vertex3(( 1,  1,  1))
#         ol.vertex3(( 1,  1, -1))
#         ol.end()
        
#         ol.begin(ol.LINESTRIP)
#         ol.vertex3(( 1, -1, -1))
#         ol.vertex3(( 1, -1,  1))
#         ol.end()
        
#         ol.begin(ol.LINESTRIP)
#         ol.vertex3((-1,  1,  1))
#         ol.vertex3((-1,  1, -1))
#         ol.end()

        #Octahedron------------------------
        ol.color3(0.0,0.0,1.0);
        ol.scale3((.8, .8, .8))
        #ol.rotate3Z(lux.time * pi * 0.1 * lux.simple_rate)
        ol.rotate3X(lux.time * pi * 0.8 * lux.simple_rate)
        #ol.rotate3Y(lux.time * pi * 0.73 * lux.simple_rate)

        for strip in self.octahedron_face_edges:
            ol.begin(ol.LINESTRIP)
            for f in strip:
                ol.vertex3(f)
            ol.end()
        
        #Tetrahedron------------------------
#         ol.color3(1.0,0.0,0.0);
#         ol.scale3((0.6, 0.6, 0.6))
#         ol.rotate3Z(lux.time * pi * 0.1 * lux.simple_rate)
#         #ol.rotate3X(lux.time * pi * 0.8 * lux.simple_rate)
#         #ol.rotate3Y(lux.time * pi * 0.73 * lux.simple_rate)

#         for strip in self.tetrahedron_face_edges:
#             ol.begin(ol.LINESTRIP)
#             for f in strip:
#                 ol.vertex3(f)
#             ol.end()





