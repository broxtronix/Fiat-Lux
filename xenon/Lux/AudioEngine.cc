#include <xenon/Lux/AudioEngine.h>
#include <xenon/Core/Exception.h>

lux::AudioEngine::AudioEngine(std::string const& jack_endpoint_name) :
  AudioClient(jack_endpoint_name), m_left_buffer(48000), m_right_buffer(48000), m_avg_buffer(48000),
  m_onset_buffer(100), m_pitch_buffer(100), 
  m_tempo_tactus_buffer(100), m_tempo_onset_buffer(100) {

  m_initialized = 0;
  
  // Set up endpoints, and connect them to the system audio input.
  this->add_input_port("in_l");
  this->add_input_port("in_r");
  this->start();

  std::ostringstream l_ostr,r_ostr;
  l_ostr << jack_endpoint_name << ":in_l";
  r_ostr << jack_endpoint_name << ":in_r";
  try {
    this->connect_ports("Soundflowerbed:out1", l_ostr.str());
    this->connect_ports("Soundflowerbed:out2", r_ostr.str());
    std::cout << "\t--> Audio Engine connected to the soundflowerbed ports.\n";
  } catch (xenon::LogicErr &e) {
    this->connect_ports("system:capture_1", l_ostr.str());
    this->connect_ports("system:capture_2", r_ostr.str());
    std::cout << "\t--> Audio Engine connected to the system capture ports.\n";
  }

  // ------------
  // Set up Aubio
  // ------------
  m_overlap_size = m_buffer_size;
  m_channels = 1;
  m_ibuf          = new_fvec(m_overlap_size, m_channels);
  m_fftgrain      = new_cvec(m_buffer_size, m_channels);
  m_onset_kl      = new_fvec(1 , m_channels);
  m_onset_complex = new_fvec(1 , m_channels);
  m_tempobuf      = new_fvec(2, m_channels);
  
  // energy,specdiff,hfc,complexdomain,phase
  m_threshold                           = 0.3;
  m_silence                             = -90.;
  m_median                              = 6;
  
  // Onset
  aubio_onsetdetection_type type_onset_kl  = aubio_onset_kl;
  aubio_onsetdetection_type type_onset_complex = aubio_onset_complex;
  m_onset_detection_kl = new_aubio_onsetdetection(type_onset_kl,m_buffer_size, m_channels);
  m_onset_detection_complex = new_aubio_onsetdetection(type_onset_complex, m_buffer_size, m_channels);
  m_peak_picker = new_aubio_peakpicker(m_threshold);
  m_phase_vocoder = new_aubio_pvoc(m_buffer_size, m_overlap_size, m_channels);

  // Pitch
  aubio_pitchdetection_type type_pitch = aubio_pitch_yinfft; // aubio_pitch_mcomb
  aubio_pitchdetection_mode mode_pitch = aubio_pitchm_freq;
  m_pitch_detection = new_aubio_pitchdetection(m_buffer_size*4, m_overlap_size, m_channels, 
                                               m_sample_rate, type_pitch, mode_pitch);
  aubio_pitchdetection_set_yinthresh(m_pitch_detection, 0.7);
  
  // FFT
  m_mfft = new_aubio_mfft(m_overlap_size, m_channels);

  // Tempo
   m_tempo = new_aubio_tempo(type_onset_complex, m_overlap_size, m_overlap_size / 4, m_channels);

  // Now that everything is set up, it's safe to start the jack callbacks.
  m_initialized = 1;
}

lux::AudioEngine::~AudioEngine() {
  m_initialized = 1;

  xenon::Mutex::Lock lock(m_mutex);
  this->stop();
  del_aubio_onsetdetection(m_onset_detection_kl);
  del_aubio_onsetdetection(m_onset_detection_complex);
  del_aubio_peakpicker(m_peak_picker);
  del_aubio_pitchdetection(m_pitch_detection);
  del_aubio_pvoc(m_phase_vocoder);
  del_aubio_mfft(m_mfft);
  //  del_aubio_tempo(m_tempo);
  del_fvec(m_tempobuf);
  del_fvec(m_ibuf);
  del_cvec(m_fftgrain);
  del_fvec(m_onset_kl);
  del_fvec(m_onset_complex);
  aubio_cleanup();
}

// Called by Jack as new audio frames arrive.  We buffer the audio
// here, and process it into summary statistics.
int lux::AudioEngine::process_callback(nframes_t nframes) {

  // Make sure we aren't shutting down.
  if (m_initialized == 0) 
    return 0;

  sample_t *i_l = (sample_t *) jack_port_get_buffer (m_ports["in_l"], nframes);
  sample_t *i_r = (sample_t *) jack_port_get_buffer (m_ports["in_r"], nframes);

  // AUDIO STORAGE
  // 
  // Store the raw audio from the left and right channel into two circular buffers
  {
    xenon::Mutex::Lock lock(m_mutex);
    for (nframes_t frm = 0; frm < nframes; frm++) {
      m_left_buffer.push_back(*i_l);
      m_right_buffer.push_back(*i_r);

      // Store the data for aubio processing
      float avg = (float(*i_l++) + float(*i_r++)) / 2.0;
      m_avg_buffer.push_back(avg);
      //      fvec_write_sample(m_ibuf, avg, 0, frm);
    }
  }

  // SILENCE DETECTION
  int is_silent = aubio_silence_detection(m_ibuf, m_silence);
   
  // ONSET DETECTION
  aubio_pvoc_do (m_phase_vocoder, m_ibuf, m_fftgrain);
  aubio_onsetdetection(m_onset_detection_complex, m_fftgrain, m_onset_kl);
  aubio_onsetdetection(m_onset_detection_complex, m_fftgrain, m_onset_complex);
  m_onset_kl->data[0][0] *= m_onset_complex->data[0][0];  
  int is_onset = aubio_peakpick_pimrt(m_onset_kl, m_peak_picker); /* ** */
  if ( is_onset && is_silent )    // Test for silence 
    is_onset = 0;   
  {
    xenon::Mutex::Lock lock(m_mutex);
    m_onset_buffer.push_back(is_onset);
  }

  // PITCH DETECTION
  smpl_t pitch = aubio_pitchdetection(m_pitch_detection, m_ibuf);  /* ** */
  {
    xenon::Mutex::Lock lock(m_mutex);
    m_pitch_buffer.push_back(pitch);
  }

  // FFT
  aubio_mfft_do (m_mfft, m_ibuf, m_fftgrain);
   
  // TEMPO (ALSO SEEMS USEFUL FOR ONSET DETECTION)
  aubio_tempo (m_tempo, m_ibuf, m_tempobuf);
  int tempo_tactus = m_tempobuf->data[0][0]; /* ** */
  int tempo_onset = m_tempobuf->data[0][1];  /* ** */
  {
    xenon::Mutex::Lock lock(m_mutex);
    m_tempo_tactus_buffer.push_back(tempo_tactus);
    m_tempo_onset_buffer.push_back(tempo_onset);
  }

  return 0;
}

void lux::AudioEngine::clear_all() {
  xenon::Mutex::Lock lock(m_mutex);

  m_left_buffer.clear();
  m_right_buffer.clear();
  m_avg_buffer.clear();    
  m_onset_buffer.clear();
  m_pitch_buffer.clear();
  m_tempo_tactus_buffer.clear();
  m_tempo_onset_buffer.clear();
}
