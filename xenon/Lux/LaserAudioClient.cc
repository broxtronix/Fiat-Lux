// This audio client drives the galvos and laser analog modulation
// (i.e. brightness).  This class acts modifyies the audio control
// signals as necessary to provide geometric and color calibration for
// the projection system.
//
#include <xenon/Lux/LaserAudioClient.h>

lux::LaserAudioClient::LaserAudioClient(std::string name) :
  AudioClient(name) {}

// Called by Jack as new audio frames arrive
int lux::LaserAudioClient::process_callback(nframes_t nframes) {

}

