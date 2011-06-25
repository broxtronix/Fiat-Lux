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

import numpy as np
cimport numpy as np
np.import_array()

from libc.stdint cimport *

cdef extern from "<string>" namespace "std":
    cdef cppclass string:
        string()
        string(char *)
        char * c_str()

cdef extern from "xenon/Lux.h" namespace "lux":
    cdef cppclass SimulatorEngine:
        SimulatorEngine(string) except +RuntimeError
        void start() except +RuntimeError
        void add_input_port(string) except +RuntimeError
        void add_output_port(string) except +RuntimeError
        void connect_ports(string, string) except +RuntimeError
        void draw_gl() except +RuntimeError
        void resize_gl(int, int) except +RuntimeError

    cdef cppclass AudioEngine:
        AudioEngine(string) except +RuntimeError
        float* get_left_buffer(int&, bool) except +RuntimeError
        float* get_right_buffer(int&, bool) except +RuntimeError
        float* get_avg_buffer(int&, bool) except +RuntimeError
        int* get_onset_buffer(int&, bool) except +RuntimeError
        float* get_pitch_buffer(int&, bool) except +RuntimeError
        int* get_tempo_tactus_buffer(int&, bool) except +RuntimeError
        int* get_tempo_onset_buffer(int&, bool) except +RuntimeError
        void clear_all() except +RuntimeError

    cdef cppclass OutputEngine:
        OutputEngine(string) except +RuntimeError
        void connect_ports(string, string) except +RuntimeError
        void setPreampCalibration(int) except +RuntimeError
        void setPreampCalibrationFrequency(float) except +RuntimeError
        void setPreampCalibrationGain(float) except +RuntimeError
        void setPreampCalibrationOffset(float) except +RuntimeError

        void setLaserCalibration(int) except +RuntimeError
        void setLaserCalibrationRedIntensity(float) except +RuntimeError
        void setLaserCalibrationGreenIntensity(float) except +RuntimeError
        void setLaserCalibrationBlueIntensity(float) except +RuntimeError
        void setLaserCalibrationXFrequency(float) except +RuntimeError
        void setLaserCalibrationYFrequency(float) except +RuntimeError

    cdef cppclass VideoEngine:
        VideoEngine(string, string) except +RuntimeError
        void draw_gl() except +RuntimeError
        void draw_lasers() except +RuntimeError
        void resize_gl(int, int) except +RuntimeError

        void setContourThreshold(float) except +RuntimeError
        void setContourBlurSigma(float) except +RuntimeError
        void setContourMinArea(float) except +RuntimeError
        void setContourMaxArea(float) except +RuntimeError
        void setContourNumConsidered(int) except +RuntimeError
        void setContourMode(int) except +RuntimeError
        void setContourMethod(int) except +RuntimeError

cdef class LuxSimulatorEngine:
    cdef SimulatorEngine *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, char *name):
        self.thisptr = new SimulatorEngine(string(name))
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

    def left_buffer(self, clear = True):
        cdef int size
        cdef float* arrsource = self.thisptr.get_left_buffer(size, clear)
        cdef np.npy_intp intp_size = size
        cdef np.ndarray newarr = np.PyArray_SimpleNewFromData(1, &intp_size, np.NPY_FLOAT, <void *>arrsource)
        return newarr.copy()

    def right_buffer(self, clear = True):
        cdef int size
        cdef float* arrsource = self.thisptr.get_right_buffer(size, clear)
        cdef np.npy_intp intp_size = size
        cdef np.ndarray newarr = np.PyArray_SimpleNewFromData(1, &intp_size, np.NPY_FLOAT, <void *>arrsource)
        return newarr.copy()

    def mono_buffer(self, clear = True):
        cdef int size
        cdef float* arrsource = self.thisptr.get_avg_buffer(size, clear)
        cdef np.npy_intp intp_size = size
        cdef np.ndarray newarr = np.PyArray_SimpleNewFromData(1, &intp_size, np.NPY_FLOAT, <void *>arrsource)
        return newarr.copy()

        
    def onset_buffer(self, clear = True):
        cdef int size
        cdef int* arrsource = self.thisptr.get_onset_buffer(size, clear)
        cdef np.npy_intp intp_size = size
        cdef np.ndarray newarr = np.PyArray_SimpleNewFromData(1, &intp_size, np.NPY_INT, <void *>arrsource)
        return newarr.copy()

    def pitch_buffer(self, clear = True):
        cdef int size
        cdef float* arrsource = self.thisptr.get_pitch_buffer(size, clear)
        cdef np.npy_intp intp_size = size
        cdef np.ndarray newarr = np.PyArray_SimpleNewFromData(1, &intp_size, np.NPY_FLOAT, <void *>arrsource)
        return newarr.copy()

    def tempo_tactus_buffer(self, clear = True):
        cdef int size
        cdef int* arrsource = self.thisptr.get_tempo_tactus_buffer(size, clear)
        cdef np.npy_intp intp_size = size
        cdef np.ndarray newarr = np.PyArray_SimpleNewFromData(1, &intp_size, np.NPY_INT, <void *>arrsource)
        return newarr.copy()

    def tempo_onset_buffer(self, clear = True):
        cdef int size
        cdef int* arrsource = self.thisptr.get_tempo_onset_buffer(size, clear)
        cdef np.npy_intp intp_size = size
        cdef np.ndarray newarr = np.PyArray_SimpleNewFromData(1, &intp_size, np.NPY_INT, <void *>arrsource)
        return newarr.copy()

    def clear_all(self):
        self.thisptr.clear_all()

cdef class LuxOutputEngine:
    cdef OutputEngine *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, char *name):
        self.thisptr = new OutputEngine(string(name))
    def __dealloc__(self):
        del self.thisptr

    def connect_ports(self, char *srcportname, char *dstportname):
        self.thisptr.connect_ports(string(srcportname), string(dstportname))

    def setPreampCalibration(self, state):
        self.thisptr.setPreampCalibration(int(state))

    def setPreampCalibrationFrequency(self, frequency):
        self.thisptr.setPreampCalibrationFrequency(frequency)

    def setPreampCalibrationGain(self, gain):
        self.thisptr.setPreampCalibrationGain(gain)

    def setPreampCalibrationOffset(self, offset):
        self.thisptr.setPreampCalibrationOffset(offset)

    def setLaserCalibration(self, state):
        self.thisptr.setLaserCalibration(int(state))

    def setLaserCalibrationRedIntensity(self, value):
        self.thisptr.setLaserCalibrationRedIntensity(value)

    def setLaserCalibrationGreenIntensity(self, value):
        self.thisptr.setLaserCalibrationGreenIntensity(value)

    def setLaserCalibrationBlueIntensity(self, value):
        self.thisptr.setLaserCalibrationBlueIntensity(value)

    def setLaserCalibrationXFrequency(self, value):
        self.thisptr.setLaserCalibrationXFrequency(value)

    def setLaserCalibrationYFrequency(self, value):
        self.thisptr.setLaserCalibrationYFrequency(value)

cdef class LuxVideoEngine:
    cdef VideoEngine *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, char *app_name, char *server_name):
        self.thisptr = new VideoEngine(string(app_name), string(server_name))
    def __dealloc__(self):
        del self.thisptr

    def draw_gl(self):
        self.thisptr.draw_gl()
    def draw_lasers(self):
        self.thisptr.draw_lasers()
    def resize_gl(self, int width, int height):
        self.thisptr.resize_gl(width, height)

    def setContourThreshold(self, value):
        self.thisptr.setContourThreshold(value)

    def setContourBlurSigma(self, value):
        self.thisptr.setContourBlurSigma(value)

    def setContourMinArea(self, value):
        self.thisptr.setContourMinArea(value)

    def setContourMaxArea(self, value):
        self.thisptr.setContourMaxArea(value)

    def setContourNumConsidered(self, value):
        self.thisptr.setContourNumConsidered(value)

    def setContourMode(self, value):
        self.thisptr.setContourMode(value)

    def setContourMethod(self, value):
        self.thisptr.setContourMethod(value)
