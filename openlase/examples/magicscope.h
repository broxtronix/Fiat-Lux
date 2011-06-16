#ifndef __LUX_MAGICSCOPE_H__
#define __LUX_MAGICSCOPE_H__

#include <jack/jack.h>
#include <map>
#include <iostream>

  // Enumerations
  typedef jack_nframes_t nframes_t;
  typedef jack_default_audio_sample_t sample_t;

  // Light-weight wrapper for the Jack audio library.
  class MagicScope {
  
    jack_client_t* m_client;
    jack_port_t *m_in_l;
    jack_port_t *m_in_r;
    jack_port_t *m_out_x;
    jack_port_t *m_out_y;
    jack_port_t *m_out_w;

    int interval;
    long nextSwitch;
    struct timeval starttime;
    sample_t* currentWave;
    sample_t* nextWave;

    protected:
      nframes_t m_sample_rate;
      nframes_t m_buffer_size;
      std::map<std::string, jack_port_t*> m_ports;
    
    public:

      // Each instance is a "client" that is registered with Jack.
      MagicScope(std::string name);
      virtual ~MagicScope();

      void add_input_port(std::string name);
      void add_output_port(std::string name);

      // ------------------------- Static Callbacks -------------------

      // This static class helps to bridge the gap between Jack's C API
      // and the world of C++.  It simply forwards the callback to this
      // instance's process_callback() method.
      static int static_process_callback(nframes_t nframes, void *instance) {
        return ((MagicScope*)instance)->process_callback(nframes);
      }

      static int static_buffer_size_callback(nframes_t nframes, void *instance) {
        return ((MagicScope*)instance)->buffer_size_callback(nframes);
      }

      static int static_sample_rate_callback(nframes_t nframes, void *instance) {
        return ((MagicScope*)instance)->sample_rate_callback(nframes);
      }

      static void static_shutdown_callback(void *instance) {
        ((MagicScope*)instance)->shutdown_callback();
      }

      // ------------------------- Instance Callbacks -------------------
      virtual int process_callback(nframes_t nframes);

      virtual int buffer_size_callback(nframes_t nframes);

      virtual int sample_rate_callback(nframes_t nframes);
      
      virtual void shutdown_callback();

  };

#endif // __LUX_MAGICSCOPE_H__
