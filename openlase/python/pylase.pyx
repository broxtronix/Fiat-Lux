#         OpenLase - a realtime laser graphics toolkit
#
# Copyright (C) 2009-2011 Hector Martin "marcan" <hector@marcansoft.com>
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

cdef extern from "libol.h":
	enum:
		OL_LINESTRIP
		OL_BEZIERSTRIP
		OL_POINTS
	enum:
		_RENDER_GRAYSCALE "RENDER_GRAYSCALE"
		_RENDER_NOREORDER "RENDER_NOREORDER"
		_RENDER_NOREVERSE "RENDER_NOREVERSE"

	ctypedef struct OLRenderParams:
		int rate
		float on_speed
		float off_speed
		int start_wait
		int start_dwell
		int curve_dwell
		int corner_dwell
		int end_dwell
		int end_wait
		float curve_angle
		float flatness
		float snap
		int render_flags
		int min_length
		int max_framelen

	ctypedef struct OLFrameInfo "OLFrameInfo":
		int objects
		int points
		int resampled_points
		int resampled_blacks
		int padding_points

	int olInit(int buffer_count, int max_points)

	void olSetRenderParams(OLRenderParams *params)
	void olGetRenderParams(OLRenderParams *params)

	ctypedef void (*AudioCallbackFunc)(float *leftbuf, float *rightbuf, int samples)

	void olSetAudioCallback(AudioCallbackFunc f)

	void olLoadIdentity()
	void olPushMatrix()
	void olPopMatrix()

	void olMultMatrix(float m[9])
	void olRotate(float theta)
	void olTranslate(float x, float y)
	void olScale(float sx, float sy)

	void olLoadIdentity3()
	void olPushMatrix3()
	void olPopMatrix3()

	void olMultMatrix3(float m[16])
	void olRotate3X(float theta)
	void olRotate3Y(float theta)
	void olRotate3Z(float theta)
	void olTranslate3(float x, float y, float z)
	void olScale3(float sx, float sy, float sz)

	void olFrustum (float left, float right, float bot, float ttop, float near, float far)
	void olPerspective(float fovy, float aspect, float zNear, float zFar)

	void olResetColor()
	void olColor3(float red, float green, float blue)
	void olMultColor(uint32_t color)
	void olPushColor()
	void olPopColor()

	void olBegin(int prim)
	void olVertex(float x, float y)
	void olVertex3(float x, float y, float z)
	void olEnd()

	void olTransformVertex3(float *x, float *y, float *z)

	ctypedef void (*ShaderFunc)(float *x, float *y, uint32_t *color)
	ctypedef void (*Shader3Func)(float *x, float *y, float *z, uint32_t *color)

	void olSetVertexPreShader(ShaderFunc f)
	void olSetVertexShader(ShaderFunc f)
	void olSetVertex3Shader(Shader3Func f)

	void olSetPixelShader(ShaderFunc f)

	void olRect(float x1, float y1, float x2, float y2)
	void olLine(float x1, float y1, float x2, float y2)
	void olDot(float x, float y, int points)

	float olRenderFrame(int max_fps) nogil

	void olGetFrameInfo(OLFrameInfo *info)

	void olShutdown()

	void olSetScissor (float x0, float y0, float x1, float y1)

	void olLog(char *fmt, ...)

	ctypedef char* const_char_ptr "const char*"
	ctypedef void (*LogCallbackFunc)(char *msg)

	void olSetLogCallback(LogCallbackFunc f)


LINESTRIP = OL_LINESTRIP
BEZIERSTRIP = OL_BEZIERSTRIP
POINTS = OL_POINTS

RENDER_GRAYSCALE = _RENDER_GRAYSCALE
RENDER_NOREORDER = _RENDER_NOREORDER
RENDER_NOREVERSE = _RENDER_NOREVERSE

C_RED	= 0xff0000
C_GREEN = 0x00ff00
C_BLUE	= 0x0000ff
C_WHITE = 0xffffff

cpdef uint32_t C_GREY(uint8_t x):
	return 0x010101 * x

cdef class RenderParams:
	cdef public int rate
	cdef public float on_speed
	cdef public float off_speed
	cdef public int start_wait
	cdef public int start_dwell
	cdef public int curve_dwell
	cdef public int corner_dwell
	cdef public int end_dwell
	cdef public int end_wait
	cdef public float curve_angle
	cdef public float flatness
	cdef public float snap
	cdef public int render_flags
	cdef public int min_length
	cdef public int max_framelen
	def __init__(self):
		self.rate = 48000
		self.on_speed = 2/100.0
		self.off_speed = 1/30.0
		self.start_wait = 8
		self.start_dwell = 3
		self.curve_dwell = 0
		self.corner_dwell = 6
		self.end_dwell = 3
		self.end_wait = 7
		self.curve_angle = 0.866
		self.flatness = 0.00001
		self.snap = 0.00001
		self.render_flags = RENDER_GRAYSCALE
		self.min_length = 0
		self.max_framelen = 0

cpdef setRenderParams(params):
	cdef OLRenderParams cparams
	cparams.rate = params.rate
	cparams.on_speed = params.on_speed
	cparams.off_speed = params.off_speed
	cparams.start_wait = params.start_wait
	cparams.start_dwell = params.start_dwell
	cparams.curve_dwell = params.curve_dwell
	cparams.corner_dwell = params.corner_dwell
	cparams.end_dwell = params.end_dwell
	cparams.end_wait = params.end_wait
	cparams.curve_angle = params.curve_angle
	cparams.flatness = params.flatness
	cparams.snap = params.snap
	cparams.render_flags = params.render_flags
	cparams.min_length = params.min_length
	cparams.max_framelen = params.max_framelen
	olSetRenderParams(&cparams)

cpdef getRenderParams():
	cdef OLRenderParams params
	olGetRenderParams(&params)
	pyparams = RenderParams()
	pyparams.rate = params.rate
	pyparams.on_speed = params.on_speed
	pyparams.off_speed = params.off_speed
	pyparams.start_wait = params.start_wait
	pyparams.start_dwell = params.start_dwell
	pyparams.curve_dwell = params.curve_dwell
	pyparams.corner_dwell = params.corner_dwell
	pyparams.end_dwell = params.end_dwell
	pyparams.end_wait = params.end_wait
	pyparams.curve_angle = params.curve_angle
	pyparams.flatness = params.flatness
	pyparams.snap = params.snap
	pyparams.render_flags = params.render_flags
	pyparams.min_length = params.min_length
	pyparams.max_framelen = params.max_framelen
	return pyparams

cpdef int init(int buffer_count=4, int max_points=30000):
	cdef int ret = olInit(buffer_count, max_points)
	if ret < 0:
		return ret
	setRenderParams(RenderParams())
	return ret

cpdef loadIdentity(): olLoadIdentity()
cpdef pushMatrix(): olPushMatrix()
cpdef popMatrix(): olPopMatrix()

cpdef multMatrix(object m):
	if len(m) == 3:
		m = m[0] + m[1] + m[2]
	cdef float cm[9]
	for i in range(9):
		cm[i] = m[i]
	olMultMatrix(cm)

cpdef rotate(float theta): olRotate(theta)
cpdef translate(tuple coord):
	x, y = coord
	olTranslate(x, y)
cpdef scale(tuple coord):
	x, y = coord
	olScale(x, y)

_py_audiocb = None
cdef void _audiocb(float *l, float *r, int samples) with gil:
	global _py_audiocb
	if _py_audiocb is not None:
		buf = _py_audiocb(samples)
		for i in range(min(len(buf), samples)):
			l[i], r[i] = buf[i]
		if len(buf) < samples:
			for i in range(len(buf), samples):
				l[i] = r[i] = 0

cpdef setAudioCallback(object func):
	global _py_audiocb
	_py_audiocb = func
	if func is not None:
		olSetAudioCallback(_audiocb)
	else:
		olSetAudioCallback(NULL)

cpdef loadIdentity3(): olLoadIdentity3()
cpdef pushMatrix3(): olPushMatrix3()
cpdef popMatrix3(): olPopMatrix3()

cpdef multMatrix3(object m):
	if len(m) == 4:
		m = m[0] + m[1] + m[2] + m[3]
	cdef float cm[16]
	for i in range(16):
		cm[i] = m[i]
	olMultMatrix(cm)

cpdef rotate3X(float theta): olRotate3X(theta)
cpdef rotate3Y(float theta): olRotate3Y(theta)
cpdef rotate3Z(float theta): olRotate3Z(theta)
cpdef translate3(tuple coord):
	x, y, z = coord
	olTranslate3(x, y, z)
cpdef scale3(tuple coord):
	x, y, z = coord
	olScale3(x, y, z)

cpdef frustum(float left, float right, float bot, float top, float near, float far):
	olFrustum(left, right, bot, top, near, far)
cpdef perspective(float fovy, float aspect, float zNear, float zFar):
	olPerspective(fovy, aspect, zNear, zFar)

cpdef resetColor(): olResetColor()
cpdef color3(float red, float green, float blue): olColor3(red, green, blue)
cpdef multColor(uint32_t color): olMultColor(color)
cpdef pushColor(): olPushColor()
cpdef popColor(): olPopColor()

cpdef begin(int prim): olBegin(prim)
cpdef vertex(tuple coord):
	x, y = coord
	olVertex(x, y)
cpdef vertex3(tuple coord):
	x, y, z = coord
	olVertex3(x, y, z)
cpdef end(): olEnd()

cpdef tuple transformVertex3(float x, float y, float z):
	olTransformVertex3(&x, &y, &z)
	return x, y, z

_py_vpreshader = None
cdef void _vpreshader(float *x, float *y, uint32_t *color) with gil:
	global _py_vpreshader
	if _py_vpreshader is not None:
		(x[0], y[0]), color[0] = _py_vpreshader((x[0], y[0]), color[0])

_py_vshader = None
cdef void _vshader(float *x, float *y, uint32_t *color) with gil:
	global _py_vshader
	if _py_vshader is not None:
		(x[0], y[0]), color[0] = _py_vshader((x[0], y[0]), color[0])

_py_v3shader = None
cdef void _v3shader(float *x, float *y, float *z, uint32_t *color) with gil:
	global _py_v3shader
	if _py_v3shader is not None:
		(x[0], y[0], z[0]), color[0] = _py_v3shader((x[0], y[0], z[0]), color[0])

_py_pshader = None
cdef void _pshader(float *x, float *y, uint32_t *color) with gil:
	global _py_pshader
	if _py_pshader is not None:
		(x[0], y[0]), color[0] = _py_pshader((x[0], y[0]), color[0])

cpdef setVertexPreShader(object func):
	global _py_vpreshader
	_py_vpreshader = func
	if func is not None:
		olSetVertexPreShader(_vpreshader)
	else:
		olSetVertexPreShader(NULL)

cpdef setVertexShader(object func):
	global _py_vshader
	_py_vshader = func
	if func is not None:
		olSetVertexShader(_vshader)
	else:
		olSetVertexShader(NULL)

cpdef setVertex3Shader(object func):
	global _py_v3shader
	_py_v3shader = func
	if func is not None:
		olSetVertex3Shader(_v3shader)
	else:
		olSetVertex3Shader(NULL)

cpdef setPixelShader(object func):
	global _py_pshader
	_py_pshader = func
	if func is not None:
		olSetPixelShader(_pshader)
	else:
		olSetPixelShader(NULL)

cpdef rect(tuple start, tuple end):
	x1, y1 = start
	x2, y2 = end
	olRect(x1, y1, x2, y2)

cpdef line(tuple start, tuple end):
	x1, y1 = start
	x2, y2 = end
	olLine(x1, y1, x2, y2)

cpdef dot(tuple coord, int points):
	x, y = coord
	olDot(x, y, points)

cpdef float renderFrame(int max_fps):
	cdef float ret
	with nogil:
		ret = olRenderFrame(max_fps)
	return ret

cdef class FrameInfo:
	cdef readonly int objects
	cdef readonly int points
	cdef readonly int resampled_points
	cdef readonly int resampled_blocks
	cdef readonly int padding_points

cpdef getFrameInfo():
	cdef OLFrameInfo info
	olGetFrameInfo(&info)
	pyinfo = FrameInfo()
	pyinfo.objects = info.objects
	pyinfo.points = info.points
	pyinfo.resampled_points = info.resampled_points
	pyinfo.resampled_blocks = info.resampled_blocks
	pyinfo.padding_points = info.padding_points
	return pyinfo

cpdef shutdown(): olShutdown()

cpdef setScissor(tuple start, tuple end):
	x1, y1 = start
	x2, y2 = end
	olSetScissor(x1, y1, x2, y2)

_py_logcb = None
cdef void _logcb(const_char_ptr msg):
	global _py_logcb
	cdef bytes msg2 = msg
	if _py_logcb is not None:
		_py_logcb(msg2)

cpdef setLogCallback(object func):
	global _py_logcb
	_py_logcb = func
	if func is not None:
		olSetLogCallback(_logcb)
	else:
		olSetLogCallback(NULL)

cdef extern from "text.h":
	ctypedef struct _Font "Font"

	_Font *olGetDefaultFont()
	float olGetCharWidth(_Font *fnt, char c)
	float olGetStringWidth(_Font *fnt, float height, char *s)
	float olGetCharOverlap(_Font *font, float height)
	float olDrawChar(_Font *fnt, float x, float y, float height, char c)
	float olDrawString(_Font *fnt, float x, float y, float height, char *s)

cdef class Font:
	cdef _Font *font

cpdef getDefaultFont():
	f = Font()
	f.font = olGetDefaultFont()
	return f

cpdef float getCharWidth(object font, char c):
	cdef Font fnt = font
	return olGetCharWidth(fnt.font, c)
cpdef float getStringWidth(object font, float height, char *s):
	cdef Font fnt = font
	return olGetStringWidth(fnt.font, height, s)
cpdef float getCharOverlap(object font, float height):
	cdef Font fnt = font
	return olGetCharOverlap(fnt.font, height)
cpdef float drawChar(object font, tuple coord, float height, char c):
	cdef Font fnt = font
	x, y = coord
	return olDrawChar(fnt.font, x, y, height, c)
cpdef float drawString(object font, tuple coord, float height, char *s):
	cdef Font fnt = font
	x, y = coord
	return olDrawString(fnt.font, x, y, height, s)

cdef extern from "ilda.h":
	ctypedef struct _IldaFile "IldaFile"

	_IldaFile *olLoadIlda(char *filename)
	void olDrawIlda(_IldaFile *ild)
	void olDrawIlda3D(_IldaFile *ild)
	void olFreeIlda(_IldaFile *ild)

cdef class IldaFile:
	cdef _IldaFile *ilda
	def __del__(self):
		olFreeIlda(self.ilda)

cpdef loadIlda(char *file):
	f = IldaFile()
	f.ilda = olLoadIlda(file)
	return f

cpdef drawIlda(object ilda):
	cdef IldaFile f = ilda
	olDrawIlda(f.ilda)

cpdef drawIlda3D(object ilda):
	cdef IldaFile f = ilda
	olDrawIlda3D(f.ilda)
