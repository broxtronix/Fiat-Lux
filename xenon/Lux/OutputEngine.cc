#include <xenon/Lux/OutputEngine.h>

lux::OutputEngine::OutputEngine(std::string const& jack_endpoint_name) :
  AudioClient(jack_endpoint_name) {
  
  // Set up endpoints, and connect them to the system audio input.
  this->add_input_port("in_x");
  this->add_input_port("in_y");
  this->add_input_port("in_r");
  this->add_input_port("in_g");
  this->add_input_port("in_b");
  this->add_input_port("in_a");

  this->add_output_port("out_x");
  this->add_output_port("out_y");
  this->add_output_port("out_r");
  this->add_output_port("out_g");
  this->add_output_port("out_b");
  this->add_output_port("out_a");
  this->add_output_port("out_s"); // safety

  m_enable_period = 44;
  m_enable_ctr = 0;

  // Set defaults
  m_transform_matrix.setIdentity();

  m_safety_first = true;

  m_swap_xy = false;
  m_invert_x = false;
  m_invert_y = false;
  m_enable_x = true;
  m_enable_y = true;

  m_blank_invert = false;
  m_blank_enable = false;
  m_output_enable = true;

  m_size_multiplier = 1.0;
  m_red_intensity_multiplier = 1.0;
  m_red_intensity_offset = 0.0;
  m_green_intensity_multiplier = 1.0;
  m_green_intensity_offset = 0.0;
  m_blue_intensity_multiplier = 1.0;
  m_blue_intensity_offset = 0.0;
}

lux::OutputEngine::~OutputEngine() {}


// Generate the 'heartbeat' square wave.
void lux::OutputEngine::generate_enable(sample_t *buf, nframes_t nframes) {
  while (nframes--) {
    if (m_enable_ctr < (m_enable_period / 2))
      *buf++ = -1.0;
    else
      *buf++ = 1.0;
    m_enable_ctr = (m_enable_ctr + 1) % m_enable_period;
  }
}

void lux::OutputEngine::transform(sample_t *ox, sample_t *oy) {
  float x = *ox;
  float y = *oy;
  
  *ox = m_transform_matrix(0,0)*x + m_transform_matrix(0,1)*y + m_transform_matrix(0,2);
  *oy = m_transform_matrix(1,0)*x + m_transform_matrix(1,1)*y + m_transform_matrix(1,2);
  float w = m_transform_matrix(2,0)*x + m_transform_matrix(2,1)*y + m_transform_matrix(2,2);
  
  *ox /= w;
  *oy /= w;
}

#define LIMIT 0.007
#define RATIO 0.30
static void cfilter(float *c, float *p)
{
  float delta = fabsf(*c - *p);
  if (delta > LIMIT) {
    if (*c > *p)
      *p = *c - LIMIT;
    else
      *p = *c + LIMIT;
  } else {
    *p = (1-RATIO) * *p + RATIO * *c;
  }
  
  *c += *c - *p;
}

// Delta filter
#define DPOWER 0.05
#define DRATIO 0.05
static void dfilter(float *c, float *p)
{
  float delta = *c - *p;
  *c += DPOWER*delta;
  
  *p = (1-DRATIO) * *p + DRATIO * *c;
}

static inline void filter(float *x, float *y)
{
  static float px=0, py=0;
  static float dx=0, dy=0;
  dfilter(x,&dx);
  dfilter(y,&dy);
  cfilter(x,&px);
  cfilter(y,&py);
}

// Called by Jack as new audio frames arrive.  We buffer the audio
// here, and process it into summary statistics.
int lux::OutputEngine::process_callback(nframes_t nframes) {
  xenon::Mutex::Lock lock(m_mutex);

  sample_t *i_x = (sample_t *) jack_port_get_buffer (m_ports["in_x"], nframes);
  sample_t *i_y = (sample_t *) jack_port_get_buffer (m_ports["in_y"], nframes);
  sample_t *i_r = (sample_t *) jack_port_get_buffer (m_ports["in_r"], nframes);
  sample_t *i_g = (sample_t *) jack_port_get_buffer (m_ports["in_g"], nframes);
  sample_t *i_b = (sample_t *) jack_port_get_buffer (m_ports["in_b"], nframes);
  sample_t *i_a = (sample_t *) jack_port_get_buffer (m_ports["in_a"], nframes);

  sample_t *o_x = (sample_t *) jack_port_get_buffer (m_ports["out_x"], nframes);
  sample_t *o_y = (sample_t *) jack_port_get_buffer (m_ports["out_y"], nframes);
  sample_t *o_r = (sample_t *) jack_port_get_buffer (m_ports["out_r"], nframes);
  sample_t *o_g = (sample_t *) jack_port_get_buffer (m_ports["out_g"], nframes);
  sample_t *o_b = (sample_t *) jack_port_get_buffer (m_ports["out_b"], nframes);
  sample_t *o_a = (sample_t *) jack_port_get_buffer (m_ports["out_a"], nframes);

  sample_t *o_s = (sample_t *) jack_port_get_buffer (m_ports["out_s"], nframes);  // Safety


  for (nframes_t frm = 0; frm < nframes; frm++) {
    sample_t x,y,r,g,b,a,orig_r,orig_g,orig_b,orig_a;
    x = *i_x++;
    y = *i_y++;
    r = orig_r = *i_r++;
    g = orig_g = *i_g++;
    b = orig_b = *i_b++;
    a = orig_a = *i_a++;

    // ---------------------
    // Adjustments to X & Y
    // ---------------------
    
    // Apply affine transformation
    y = -y;
    this->transform(&x, &y);
    y = -y;
    
    // Swap, or invert X & Y
    if (m_swap_xy) {
      sample_t tmp = x;
      x = y;
      y = tmp;
    }
    if (m_invert_x)
      x = -x;
    if (m_invert_y)
      y = -y;
    if (!(m_enable_x) && !m_safety_first)
      x = 0.0f;
    if (!(m_enable_y) && !m_safety_first)
      y = 0.0f;
    if (m_safety_first && m_size_multiplier < 0.10f) {
      x *= 0.10f;
      y *= 0.10f;
    } else {
      x *= m_size_multiplier;
      y *= m_size_multiplier;
    }

    // Run the openlase filters 
    //
    // **** TODO: What does this do??
    //filter(&x, &y);
    
    *o_x++ = x;
    *o_y++ = y;

    // ------------------------
    // Adjustments to r,g, & b
    // ------------------------

    // Adjust blanking and global laser intensity values.
    if (m_blank_invert) {
      r = 1.0f - r;
      g = 1.0f - g;
      b = 1.0f - b;
    }
    if (!(m_blank_enable)) {
      r = 1.0f;
      g = 1.0f;
      b = 1.0f;
    }
    if (!(m_output_enable)) {
      r = 0.0f;
      g = 0.0f;
      b = 0.0f;
    }
    r *= m_red_intensity_multiplier * (1.0f-m_red_intensity_offset);
    r += m_red_intensity_offset;
    g *= m_green_intensity_multiplier * (1.0f-m_green_intensity_offset);
    g += m_green_intensity_offset;
    b *= m_blue_intensity_multiplier * (1.0f-m_blue_intensity_offset);
    b += m_blue_intensity_offset;

    // Limit the max output, just in case!
    if (r > 1.0) r = 1.0;
    if (g > 1.0) g = 1.0;
    if (b > 1.0) b = 1.0;

    if(orig_r != 0.0f || orig_g != 0 || orig_b != 0) {
      m_frames_dead = 0;
    } else if (m_frames_dead < m_dead_time) {
      m_frames_dead++;
    } else {
      r = 0.0f;
      g = 0.0f;
      b = 0.0f;
    }

    *o_r++ = r;
    *o_g++ = g;
    *o_b++ = b;
    *o_a++ = a;
  }
  this->generate_enable(o_s, nframes);
  return 0;
}

// Set sample rate
int lux::OutputEngine::sample_rate_callback(nframes_t nframes) {
  m_sample_rate = nframes;

  m_enable_period = int(nframes / 1000);
  m_enable_ctr = 0;

  m_frames_dead = 0;
  m_dead_time = (m_sample_rate/10);
}
