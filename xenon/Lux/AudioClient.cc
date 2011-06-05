#include <xenon/Lux/AudioClient.h>
#include <xenon/Core/Log.h>
#include <xenon/Core/Exception.h>
using namespace xenon;

lux::AudioClient::AudioClient(std::string name) : m_sample_rate(0), m_buffer_size(0) {
  if ((m_client = jack_client_new (name.c_str())) == 0) {
    xenon_throw( LogicErr() << "Failed to start AudioClient -- could not iniitialize Jack.  Is the Jack server running?" );
  }

  jack_set_process_callback (m_client, AudioClient::static_process_callback, this);
  jack_set_buffer_size_callback (m_client, AudioClient::static_buffer_size_callback, this);
  jack_set_sample_rate_callback (m_client, AudioClient::static_sample_rate_callback, this);
  jack_on_shutdown (m_client, AudioClient::static_shutdown_callback, this);
}

lux::AudioClient::~AudioClient() {
  jack_client_close (m_client);
}

void lux::AudioClient::add_input_port(std::string name) {
  m_ports[name] = jack_port_register (m_client, name.c_str(), JACK_DEFAULT_AUDIO_TYPE, JackPortIsInput, 0);
}

void lux::AudioClient::add_output_port(std::string name) {
  m_ports[name] = jack_port_register (m_client, name.c_str(), JACK_DEFAULT_AUDIO_TYPE, JackPortIsOutput, 0);
}

void lux::AudioClient::start() const {
  if (jack_activate (m_client)) {
    xenon_throw( LogicErr() << "Cannot activate AudioClient" );
  }
}
