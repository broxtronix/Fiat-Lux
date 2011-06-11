// This audio client drives the galvos and laser analog modulation
// (i.e. brightness).  This class acts modifyies the audio control
// signals as necessary to provide geometric and color calibration for
// the projection system.
//
#ifndef __LUX_LASER_AUDIOCLIENT_H__
#define __LUX_LASER_AUDIOCLIENT_H__

#include <xenon/Lux/AudioClient.h>
#include <string>

namespace lux {

  class LaserClient : public AudioClient {

  public:
    
    LaserClient(std::string name);
    virtual ~LaserClient() {}

    // Called by Jack as new audio frames arrive
    virtual int process_callback(nframes_t nframes);
  };

}

#endif // __LUX_LASER_AUDIOCLIENT_H__
