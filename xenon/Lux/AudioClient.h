#ifndef __LUX_AUDIOCLIENT_H__
#define __LUX_AUDIOCLIENT_H__

#include <jack/jack.h>
#include <map>
#include <iostream>

namespace lux {

  // Enumerations
  typedef jack_nframes_t nframes_t;
  typedef jack_default_audio_sample_t sample_t;

  // Light-weight wrapper for the Jack audio library.
  class AudioClient {
  
    jack_client_t* m_client;

  protected:
    nframes_t m_sample_rate;
    nframes_t m_buffer_size;
    std::map<std::string, jack_port_t*> m_ports;
    
  public:

    // Each instance is a "client" that is registered with Jack.
    AudioClient(std::string name);
    virtual ~AudioClient();

    void add_input_port(std::string const& name);
    void add_output_port(std::string const& name);

    // Connect ports using the "<name>:<portname" port naming
    // convention.  For example, you could connect "lux_engine:out_x"
    // to "lux_simulator:in_x".
    void connect_ports(std::string const& src_port, std::string const& dst_port);

    virtual void start() const;
    virtual void stop();

    // ------------------------- Static Callbacks -------------------

    // This static class helps to bridge the gap between Jack's C API
    // and the world of C++.  It simply forwards the callback to this
    // instance's process_callback() method.
    static int static_process_callback(nframes_t nframes, void *instance) {
      return ((AudioClient*)instance)->process_callback(nframes);
    }

    static int static_buffer_size_callback(nframes_t nframes, void *instance) {
      return ((AudioClient*)instance)->buffer_size_callback(nframes);
    }

    static int static_sample_rate_callback(nframes_t nframes, void *instance) {
      return ((AudioClient*)instance)->sample_rate_callback(nframes);
    }

    static void static_shutdown_callback(void *instance) {
      ((AudioClient*)instance)->shutdown_callback();
    }

    // ------------------------- Instance Callbacks -------------------
    virtual int process_callback(nframes_t nframes) {
      // do nothing in default implementation
      return 0;
    }

    virtual int buffer_size_callback(nframes_t nframes) {
      m_buffer_size = nframes;
      return 0;
    }

    virtual int sample_rate_callback(nframes_t nframes) {
      m_sample_rate = nframes;
      return 0;
    }

    virtual void shutdown_callback() {
      // do nothing in default implementation
    }

  };
} // namespace lux

#endif // __LUX_AUDIOCLIENT_H__
