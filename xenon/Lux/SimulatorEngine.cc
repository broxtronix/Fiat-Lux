#include <xenon/Lux/SimulatorEngine.h>
#include <jack/jack.h>
#include <math.h>

#ifdef __APPLE__
#include <OpenGL/gl.h>
#include <OpenGL/glu.h>
#include <AGL/agl.h>
#else // Linux
#include <GL/gl.h>
#include <GL/glu.h>
#endif

lux::SimulatorEngine::SimulatorEngine(std::string name) : 
      AudioClient(name), m_buf_widx(0), m_psize(2) {

  this->add_input_port("in_x");
  this->add_input_port("in_y");
  this->add_input_port("in_r");
  this->add_input_port("in_g");
  this->add_input_port("in_b");
  this->add_input_port("in_a");
  
// #ifdef __APPLE__
//   AGLContext aglContext;
//   aglContext = aglGetCurrentContext();
//   GLint swapInt = 1;
//   aglSetInteger(aglContext, AGL_SWAP_INTERVAL, &swapInt);
// #endif
  
}

 void lux::SimulatorEngine::laser_color(float r, float g, float b, float ascale) {

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

void lux::SimulatorEngine::draw_gl() {
  int i, ridx;

  static int fno=0;
  fno++;
  glClearColor(0.0,0.0,0.0,1.0);
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glLoadIdentity();
  glLineWidth(m_psize);
  glPointSize(m_psize);

  ridx = (m_buf_widx - LUX_SIMULATOR_HIST_SAMPLES + LUX_SIMULATOR_BUF_SAMPLES) % LUX_SIMULATOR_BUF_SAMPLES;
        
  float lx, ly, lr, lg, lb;
  lx = ly = lr = lg = lb = 0;

  float rdelay[2] = {0,0};
  float gdelay[2] = {0,0};
  float bdelay[2] = {0,0};
  
  for (i = 0; i<LUX_SIMULATOR_HIST_SAMPLES; i++) {
    float r, g, b;

    bufsample_t s = m_buffer[ridx];
    // lowpass
    s.x = lx * 0.65 + s.x * 0.35;
    s.y = ly * 0.65 + s.y * 0.35;
    // delay brightness
    rdelay[i%2] = s.r;
    gdelay[i%2] = s.g;
    bdelay[i%2] = s.b;
    s.r = rdelay[(i+1)%2];
    s.g = gdelay[(i+1)%2];
    s.b = bdelay[(i+1)%2];
    
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
      r = (s.r-0.2) * factor * dfactor * 1.8;
      g = (s.g-0.2) * factor * dfactor * 1.8;
      b = (s.b-0.2) * factor * dfactor * 1.8;
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

void lux::SimulatorEngine::resize_gl(int width, int height) {
  if (width == 0 || height == 0) {
    width = 512;  height = 512;
  }
  int min = width > height ? height : width;
  glViewport((width-min)/2, (height-min)/2, min, min);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glOrtho (-1, 1, -1, 1, -1, 1);
  glMatrixMode(GL_MODELVIEW);
}

 int lux::SimulatorEngine::process_callback(nframes_t nframes) {
  sample_t *i_x = (sample_t *) jack_port_get_buffer (m_ports["in_x"], nframes);
  sample_t *i_y = (sample_t *) jack_port_get_buffer (m_ports["in_y"], nframes);
  sample_t *i_r = (sample_t *) jack_port_get_buffer (m_ports["in_r"], nframes);
  sample_t *i_g = (sample_t *) jack_port_get_buffer (m_ports["in_g"], nframes);
  sample_t *i_b = (sample_t *) jack_port_get_buffer (m_ports["in_b"], nframes);
  sample_t *i_a = (sample_t *) jack_port_get_buffer (m_ports["in_a"], nframes);

  for (nframes_t frm = 0; frm < nframes; frm++) {
    m_buffer[m_buf_widx].x = *i_x++;
    m_buffer[m_buf_widx].y = *i_y++;
    m_buffer[m_buf_widx].r = *i_r++;
    m_buffer[m_buf_widx].g = *i_g++;
    m_buffer[m_buf_widx].b = *i_b++;
    m_buffer[m_buf_widx].a = *i_a++;
    
    m_buf_widx++;
    if (m_buf_widx >= LUX_SIMULATOR_BUF_SAMPLES)
      m_buf_widx = 0;
  }
  
  return 0;
}

