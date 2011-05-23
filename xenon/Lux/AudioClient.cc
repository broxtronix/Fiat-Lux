#include <xenon/Lux/AudioClient.h>
#include <xenon/Core/Log.h>
#include <xenon/Core/Exception.h>
using namespace xenon;

lux::AudioClient::AudioClient(std::string name) : m_sample_rate(0), m_buffer_size(0) {
  if ((m_client = jack_client_new (name.c_str())) == 0) {
    xenon_throw( LogicErr() << "Failed to start AudioClient -- could not iniitialize Jack.  Is the Jack server running?" );
  }
}

lux::AudioClient::~AudioClient() {
  jack_client_close (m_client);
}

void lux::AudioClient::add_port(std::string name, audio_client_channel_type type) {
  if (type == AUDIO_CLIENT_INPUT) {
    m_ports[name] = jack_port_register (m_client, name.c_str(), JACK_DEFAULT_AUDIO_TYPE, JackPortIsInput, 0);
  } else {
    m_ports[name] = jack_port_register (m_client, name.c_str(), JACK_DEFAULT_AUDIO_TYPE, JackPortIsOutput, 0);
  }
}

void lux::AudioClient::start() const {
  if (jack_activate (m_client)) {
    xenon_throw( LogicErr() << "Cannot activate AudioClient" );
  }
}
