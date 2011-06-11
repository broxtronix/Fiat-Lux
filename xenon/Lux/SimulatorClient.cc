#include <xenon/Lux/SimulatorClient.h>
#include <jack/jack.h>
#include <math.h>

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#endif

 void lux::SimulatorClient::laser_color(float r, float g, float b, float ascale) {

   // This was the original laser_color code.  
   //   float r, b;
   //   r = b = 0;
   //   if (g < 0)
   //     g = 0;
   //   if (g > 2.0)
   //     g = 2.0;
   //   if (g > 1.0) {
   //     r = b = g - 1.0;
   //     g = 1.0;
   //   }
   //   glColor4f(r, 1, b, g*ascale);
   
  glColor4f(r, g, b, ascale);
}

void lux::SimulatorClient::draw_gl() {
  int i, ridx;

  static int fno=0;
  fno++;
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glLoadIdentity();
  glLineWidth(m_psize);
  glPointSize(m_psize);

  ridx = (m_buf_widx - LUX_SIMULATOR_HIST_SAMPLES + LUX_SIMULATOR_BUF_SAMPLES) % LUX_SIMULATOR_BUF_SAMPLES;
        
  float lx, ly, lr, lg, lb;
  lx = ly = lr = lg = lb = 0;

  float gdelay[2] = {0,0};
  
  for (i = 0; i<LUX_SIMULATOR_HIST_SAMPLES; i++) {
    float r, g, b;

    bufsample_t s = m_buffer[ridx];
    // lowpass
    s.x = lx * 0.65 + s.x * 0.35;
    s.y = ly * 0.65 + s.y * 0.35;
    // delay brightness
    gdelay[i%2] = s.g;
    s.g = gdelay[(i+1)%2];
    
    float d = sqrtf((s.x-lx)*(s.x-lx) + (s.y-ly)*(s.y-ly));
    if (d == 0)
      d = 0.0001;
    float dfactor = 0.01/d;
    if (dfactor > 1.5)
      dfactor = 1.5;
    
    int age = LUX_SIMULATOR_HIST_SAMPLES-i;
    float factor;
    
    factor = (LUX_SIMULATOR_HIST_SAMPLES-age)/(float)LUX_SIMULATOR_HIST_SAMPLES;
    factor = factor*factor;
    
    if (fabsf(s.x-lx) < 0.001 && fabsf(s.y-ly) < 0.001) {
      r = (s.r-0.2) * factor * 1.4;
      g = (s.g-0.2) * factor * 1.4;
      b = (s.b-0.2) * factor * 1.4;
      glBegin(GL_POINTS);
      laser_color(r, g, b, 0.08);
      glVertex3f(s.x, s.y, 0);
      glEnd();
    } else {
      g = (s.g-0.2) * factor * dfactor * 1.8;
      glBegin(GL_LINES);
      laser_color(lr, lg, lb, 0.8);
      glVertex3f(lx, ly, 0);
      laser_color(r, g, b, 0.8);
      glVertex3f(s.x, s.y, 0);
      glEnd();
    }
    
    lx = s.x;
    ly = s.y;
    lr = r;
    lg = g;
    lb = b;
    
    ridx++;
    if (ridx >= LUX_SIMULATOR_BUF_SAMPLES)
      ridx = 0;
  }
  glEnd();
}

void lux::SimulatorClient::resize_gl(int width, int height) {
  int min = width > height ? height : width;
  glViewport((width-min)/2, (height-min)/2, min, min);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glOrtho (-1, 1, -1, 1, -1, 1);
  glMatrixMode(GL_MODELVIEW);
}

 int lux::SimulatorClient::process_callback(nframes_t nframes) {
  sample_t *i_x = (sample_t *) jack_port_get_buffer (m_ports["in_x"], nframes);
  sample_t *i_y = (sample_t *) jack_port_get_buffer (m_ports["in_y"], nframes);
  sample_t *i_r = (sample_t *) jack_port_get_buffer (m_ports["in_r"], nframes);
  sample_t *i_g = (sample_t *) jack_port_get_buffer (m_ports["in_g"], nframes);
  sample_t *i_b = (sample_t *) jack_port_get_buffer (m_ports["in_b"], nframes);

  for (nframes_t frm = 0; frm < nframes; frm++) {
    m_buffer[m_buf_widx].x = *i_x++;
    m_buffer[m_buf_widx].y = *i_y++;
    m_buffer[m_buf_widx].r = *i_r++;
    m_buffer[m_buf_widx].g = *i_g++;
    m_buffer[m_buf_widx].b = *i_b++;
    
    m_buf_widx++;
    if (m_buf_widx >= LUX_SIMULATOR_BUF_SAMPLES)
      m_buf_widx = 0;
  }
  
  return 0;
}

