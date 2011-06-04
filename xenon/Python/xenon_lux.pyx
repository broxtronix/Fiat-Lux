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
    cdef cppclass SimulatorAudioClient:
        SimulatorAudioClient(string)
        void test()

cdef class LuxSimulatorAudioClient:
    cdef SimulatorAudioClient *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, char *name):
        self.thisptr = new SimulatorAudioClient(string(name))
    def __dealloc__(self):
        del self.thisptr
    def test(self):
        self.thisptr.test()



