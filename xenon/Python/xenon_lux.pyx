# Copyright (C) 2011 Michael Broxton (broxton@stanford.edu)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 or version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

from libc.stdint cimport *

cdef extern from "<string>" namespace "std":
    cdef cppclass string:
        string()
        string(char *)
        char * c_str()
     
cdef extern from "xenon/Lux.h" namespace "lux":
    cdef cppclass SimulatorClient:
        SimulatorClient(string) except +RuntimeError
        void start() except +RuntimeError
        void add_input_port(string) except +RuntimeError
        void add_output_port(string) except +RuntimeError
        void connect_ports(string, string) except +RuntimeError
        void draw_gl() except +RuntimeError
        void resize_gl(int, int) except +RuntimeError

    cdef cppclass AudioEngine:
        AudioEngine(string) except +RuntimeError

cdef class LuxSimulatorClient:
    cdef SimulatorClient *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, char *name):
        self.thisptr = new SimulatorClient(string(name))
    def __dealloc__(self):
        del self.thisptr

    def add_input_port(self, char *portname):
        self.thisptr.add_input_port(string(portname))
    def add_output_port(self, char *portname):
        self.thisptr.add_output_port(string(portname))
    def connect_ports(self, char *srcportname, char *dstportname):
        self.thisptr.connect_ports(string(srcportname), string(dstportname))

    def start(self):
        self.thisptr.start()

    def draw_gl(self):
        self.thisptr.draw_gl()
    def resize_gl(self, int width, int height):
        self.thisptr.resize_gl(width, height)



cdef class LuxAudioEngine:
    cdef AudioEngine *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, char *name):
        self.thisptr = new AudioEngine(string(name))
    def __dealloc__(self):
        del self.thisptr
        
