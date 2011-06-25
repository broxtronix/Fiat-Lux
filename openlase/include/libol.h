/*
        OpenLase - a realtime laser graphics toolkit

Copyright (C) 2009-2011 Hector Martin "marcan" <hector@marcansoft.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 or version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/

#ifndef LIBOL_H
#define LIBOL_H

#include <stdint.h>

enum {
	OL_LINESTRIP,
	OL_BEZIERSTRIP,
	OL_POINTS
};

#define C_RED   0xff0000
#define C_GREEN 0x00ff00
#define C_BLUE  0x0000ff
#define C_WHITE 0xffffff
#define C_BLACK 0x000000

#define C_GREY(x)   (0x010101 * ((int)(x)))

enum {
	RENDER_GRAYSCALE = 1,
	RENDER_NOREORDER = 2,
	RENDER_NOREVERSE = 4,
};

typedef struct {
  int rate;         // Sets the max sampling rate for the system.
                    // Does nothing except determine how many points
                    // will be inserted as necessary to meet this
                    // framerate.
  float on_speed;   // Speed at which the laser moves when it is on.
                    // Measured in screen distance per point. For
                    // example, on_speed = 1/100 would draw 200 points
                    // as the laser crosses the screen.  Ensures
                    // constant brightness.
  float off_speed;  // Speed the laser moves when it is off, mesaure
                    // in screen distance per point.
  int start_wait;
  int start_dwell;  // Number of samples to dwell at the beginning of each point or path.  
  int curve_dwell;  // Number of samples to dwell if dot > curve_angle
  int corner_dwell; // Number of samples to dwell in the corner of an object
  int end_dwell;    // Number of samples to dwell at the end of each point or bath by olEnd()
  int end_wait;
  float curve_angle;
  float flatness;   // Determines when to subdivide bezier curves
  float snap;       
  int render_flags;
  int min_length;   // Minimum length (in points) for a path to be drawn. 
  int max_framelen;
} OLRenderParams;

typedef struct {
	int objects;
	int points;
	int resampled_points;
	int resampled_blacks;
	int padding_points;
} OLFrameInfo;

int olInit(int buffer_count, int max_points);

void olSetRenderParams(OLRenderParams *params);
void olGetRenderParams(OLRenderParams *params);

typedef void (*AudioCallbackFunc)(float *leftbuf, float *rightbuf, int samples);

void olSetAudioCallback(AudioCallbackFunc f);

void olLoadIdentity(void);
void olPushMatrix(void);
void olPopMatrix(void);

void olMultMatrix(float m[9]);
void olRotate(float theta);
void olTranslate(float x, float y);
void olScale(float sx, float sy);

void olLoadIdentity3(void);
void olPushMatrix3(void);
void olPopMatrix3(void);

void olMultMatrix3(float m[16]);
void olRotate3X(float theta);
void olRotate3Y(float theta);
void olRotate3Z(float theta);
void olTranslate3(float x, float y, float z);
void olScale3(float sx, float sy, float sz);

void olFrustum (float left, float right, float bot, float ttop, float near, float far);
void olPerspective(float fovy, float aspect, float zNear, float zFar);

void olResetColor(void);
void olMultColor(uint32_t color);
void olColor3(float red, float green, float blue);
void olColor(uint32_t color);
void olPushColor(void);
void olPopColor(void);

void olBegin(int prim);
void olVertex(float x, float y);
void olVertex3(float x, float y, float z);
void olEnd(void);

void olTransformVertex3(float *x, float *y, float *z);

typedef void (*ShaderFunc)(float *x, float *y, uint32_t *color);
typedef void (*Shader3Func)(float *x, float *y, float *z, uint32_t *color);

void olSetVertexPreShader(ShaderFunc f);
void olSetVertexShader(ShaderFunc f);
void olSetVertex3Shader(Shader3Func f);

void olSetPixelShader(ShaderFunc f);

void olRect(float x1, float y1, float x2, float y2);
void olLine(float x1, float y1, float x2, float y2);
void olDot(float x, float y, int points);
float olRenderFrame(int max_fps);

void olGetFrameInfo(OLFrameInfo *info);

void olShutdown(void);

void olSetScissor (float x0, float y0, float x1, float y1);

void olLog(const char *fmt, ...);

typedef void (*LogCallbackFunc)(const char *msg);

void olSetLogCallback(LogCallbackFunc f);

#endif
