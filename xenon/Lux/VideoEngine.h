#ifndef __LUX_VIDEO_ENGINE_H__
#define __LUX_VIDEO_ENGINE_H__

#include <xenon/Lux/AudioClient.h>
#include <xenon/Graphics/SyphonClient.h>
#include <string>
#include <iostream>

namespace lux {

  class VideoEngine {
    
    xenon::graphics::XenonSyphonClient m_syphon_client;

  public:

    VideoEngine(std::string application_name, std::string server_name);
    virtual ~VideoEngine() {} 

    void draw_gl();
    void resize_gl(int width, int height);
  };

}

#endif // __LUX_VIDEO_ENGINE_H__
